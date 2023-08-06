__author__ = "Pawel Kowalik"
__copyright__ = "Copyright 2018, 1&1 IONOS SE"
__credits__ = ["Andreea Dima", "Marc Laue"]
__license__ = "MIT"
__maintainer__ = "Pawel Kowalik"
__email__ = "pawel-kow@users.noreply.github.com"
__status__ = "Beta"

import cgi
import datetime
import hashlib
import json
import logging
from uuid import uuid4

from dns.exception import Timeout
from dns.resolver import Resolver, NXDOMAIN, YXDOMAIN, NoAnswer, NoNameservers
from jwcrypto import jwt, jwk, jwe
from jwcrypto.common import JWException
from six.moves import urllib

from id4me_rp_client.helper.stringify_keys import stringify_keys
from .id4me_constants import OIDCApplicationType, OIDCScopeToClaim
from .id4me_exceptions import *
from .network import get_json_auth, post_json, post_data, NetworkContext, http_request

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

_jws_alg_map = {
    "HS256": "oct",
    "HS384": "oct",
    "HS512": "oct",
    "RS256": "RSA",
    "RS384": "RSA",
    "RS512": "RSA",
    "ES256": "ES",
    "ES384": "ES",
    "ES512": "ES",
}


class TokenDecodeType(object):
    IDToken = 1
    UserInfo = 2
    Other = 3


class ID4meContext(object):
    def __init__(self, id4me, identity_authority, issuer):
        """
        Constructs ID4me context
        :param id4me: identifier
        :type id4me: str
        :param identity_authority: identity authority identifier
        :type identity_authority: str
        :param issuer: OIDC issuer
        :type issuer: str
        """
        self.id = id4me
        self.iau = identity_authority
        self.issuer = issuer
        self.access_token = None
        self.refresh_token = None
        self.iss = None
        self.sub = None
        self.nonce = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def from_json(json_string):
        jsonobj = json.loads(json_string)
        ctx = ID4meContext(
            id4me=jsonobj['id'],
            identity_authority=jsonobj['iau'],
            issuer=jsonobj['issuer']
        )
        ctx.access_token = jsonobj.get('access_token', None)
        ctx.refresh_token = jsonobj.get('refresh_token', None)
        ctx.iss = jsonobj.get('iss', None)
        ctx.sub = jsonobj.get('sub', None)
        ctx.nonce = jsonobj.get('nonce', None)
        return ctx


class ID4meClaimsRequest(object):
    def __init__(self, id_token_claims=None, userinfo_claims=None):
        """
        :param id_token_claims: dictionary of claims requested from identity authority in id_token as dict(claim_name->str, properties->ID4meClaimRequestProperties=None)
        :type id_token_claims: dict
        :param userinfo_claims: dictionary of claims requested from identity agent through user_info as dict(claim_name->str, properties->ID4meClaimRequestProperties=None)
        :type userinfo_claims: dict
        """
        if id_token_claims is not None:
            self.id_token = id_token_claims
        if userinfo_claims is not None:
            self.userinfo = userinfo_claims


class ID4meClaimRequestProperties(object):
    def __init__(self, essential=None, reason=None):
        """
        Optional properties of claim request
        :param essential: specify if the claim is essential or optional
        :type essential: bool
        :param reason: specify reason for the claim request
        :type reason: str
        """
        if essential is not None:
            self.essential = essential
        if reason is not None:
            self.reason = reason


class ID4meClient(object):
    def __init__(self, validate_url,
                 client_name,
                 get_client_registration,
                 save_client_registration=None,
                 jwks_url=None,
                 app_type=OIDCApplicationType.native,
                 preferred_client_id=None,
                 logo_url=None,
                 policy_url=None,
                 tos_url=None,
                 private_jwks_json=None,
                 network_context=None,
                 requireencryption=None,
                 register_client_dynamically=True,
                 use_scope_if_claims_not_supported=True,
                 require_id_token_signing=True,
                 require_user_info_signing=None,
                 authority_lookup_override=None):
        """
        Constructor of ID4me Client, providing the data for client registration if needed
        :type register_client_dynamically: object
        :param validate_url: redirect uri after successful login
        :type validate_url: str
        :param client_name: displayed client name
        :type client_name: str
        :param get_client_registration: callback to lookup authority registration of the form ``callback(authority_name->str)->str``
        :type get_client_registration: function
        :param save_client_registration: callback to save authority settings of the form ``callback(authority_name->str, authority_registration->str)->None``
        :type save_client_registration: function
        :param jwks_url: (optional) url of the public key jwks - only needed if encryption needed
        :type jwks_url: str
        :param app_type: application type native or web, default native
        :type app_type: OIDCApplicationType
        :param preferred_client_id: DEPRECATED: preferred client ID (not supported by Authporities, no effect)
        :type preferred_client_id: str
        :param logo_url: (optional) logo URL (must be same domain name)
        :type logo_url: str
        :param policy_url: (optional) policy URL (must be same domain name)
        :type policy_url: str
        :param tos_url: (optional) T&C URL (must be same domain name)
        :type tos_url: str
        :param private_jwks_json: (optional) public key jwks encoded as JSON - only needed if encryption needed
        :type private_jwks_json: str
        :param requireencryption: if encryption is to be enforced. True = Always, False = Never, None = best efforts
        :type requireencryption: bool
        :param network_context: network context to adjust DNS resolvers or SSL Proxy
        :type network_context: NetworkContext
        :param register_client_dynamically: specify if OIDC Dynamic Client Registration shall be performed if client missing or expired
        :type register_client_dynamically: bool
        :param use_scope_if_claims_not_supported: specify if scopes shall be used to get user claims if IdP does not specify claims_parameter_supported
        :type use_scope_if_claims_not_supported: bool
        :param require_id_token_signing: specify, if always use id_token_signed_response_alg parameter when registering
                    client. true - parameter is always set to supported alg. False - parameter is set to "none"
                    None - parameter is not used (IdP defaults are taken)
        :type require_id_token_signing: bool
        :param require_user_info_signing: specify, if always use user_info_signed_response_alg parameter when registering
                    client. true - parameter is always set to supported alg. False - parameter is set to "none"
                    None - parameter is not used (IdP defaults are taken)
        :type require_user_info_signing: bool
        :param authority_lookup_override: callback which allows to override the DNS authority lookup ``callback(identifier->str)->str``
                    If None returned, then regular DNS lookup will be perfomed
        :type authority_lookup_override: function
        :rtype: ID4meClient
        """
        self.validateUrl = validate_url
        self.jwksUrl = jwks_url
        self.client_name = client_name
        self.preferred_client_id = preferred_client_id
        self.logoUrl = logo_url
        self.policyUrl = policy_url
        self.tosUrl = tos_url
        self.private_jwks = None
        if private_jwks_json is not None:
            self.private_jwks = jwk.JWKSet.from_json(private_jwks_json)
        self.requireencryption = requireencryption

        if (self.requireencryption and self.private_jwks is None):
            logger.debug('Encryption required but private_jwks_json specified')
            raise ID4meException('Encryption required but private_jwks_json specified')

        if network_context is not None:
            self.networkContext = network_context
        else:
            self.networkContext = NetworkContext(max_bytes=50*1024)
        self.app_type = app_type

        self.resolver = Resolver()
        if (self.networkContext.nameservers is not None):
            self.resolver.nameservers = self.networkContext.nameservers

        self.get_client_registration = get_client_registration
        self.save_client_registration = save_client_registration
        self.register_client_dynamically = register_client_dynamically
        self.use_scope_if_claims_not_supported = use_scope_if_claims_not_supported
        self.require_id_token_signing = require_id_token_signing
        self.require_user_info_signing = require_user_info_signing
        self.authority_lookup_override = authority_lookup_override

    @staticmethod
    def _get_domain_name_to_lookup(id4me):
        """
        Transforms the provided identifier into domain name to lookup (for example local-part hash for E-mails)
        :param id4me: original identifier
        :type id4me: str
        :returns transformed identifier for lookup
        :rtype str
        """
        if '@' in id4me:
            parts = id4me.split('@')
            if len(parts) == 2:
                localhashed = hashlib.sha256(parts[0].encode(encoding='UTF-8')).hexdigest()[:56]
                return '{}.{}'.format(localhashed, parts[1])
            else:
                logger.debug('Invalid identifier: {}'.format(id4me))
                raise ID4meInvalidIDException('Invalid identifier: {}'.format(id4me))
        else:
            return id4me



    def _get_identity_authority(self, id4me):
        """
        Finds authority responsible for a given id4me
        :param id4me: identifier
        :type id4me: str
        :return: identity authority identifier (FQDN or URL)
        :rtype: str
        """

        if self.authority_lookup_override is not None:
            overridden_lookup = self.authority_lookup_override(id4me)
            if overridden_lookup is not None:
                return overridden_lookup

        parts = self._get_domain_name_to_lookup(id4me).split('.')
        first_exception = None
        for idx in range(0, len(parts)):
            lab = '.'.join(parts[idx:])
            if len(lab) > 0:
                try:
                    return self._get_identity_authority_once(lab)
                except Exception as e:
                    if first_exception is None:
                        first_exception = e
                    
        if first_exception is not None:
            raise first_exception
        else:
            logger.debug('All options checked but no TXT DNS entry found for {} or its parents'.format(id4me))
            raise ID4meDNSResolverException('All options checked but no TXT DNS entry found for {} or its parents'.format(id4me))

    def _get_identity_authority_once(self, domain):
        """
        Makes a single resolution of _openid DNS record of given domain name
        :param domain: domain name
        :type domain: str
        :return: Identity authority stored for domain name
        :rtype: str
        :raise ID4meDNSResolverException: if DNS resolution not possible or record missing/invalid
        """
        hostname = '_openid.{}.'.format(domain)
        logger.debug('Resolving "{}"'.format(hostname))
        try:
            dns_resolver = self.resolver.query(hostname, 'TXT')
            # TODO: enforce strict DNSSEC policy when support added by all parties...
            # self._check_dns_sec(id)
            for txt in dns_resolver:
                value = str(txt).replace('"', '')
                logger.debug('Checking TXT record "{}"'.format(value))
                if not value.startswith('v=OID1;'):
                    continue
                for item in value.split(';'):
                    if item.startswith('iss='):
                        return item[4:]
        except Timeout:
            logger.debug('Timeout. Failed to resolve "{}"'.format(hostname))
            raise ID4meDNSResolverException('Timeout. Failed to resolve "{}"'.format(hostname))
        except NXDOMAIN:
            logger.debug('Failed to resolve "{}"'.format(hostname))
            raise ID4meDNSResolverException('Failed to resolve "{}"'.format(hostname))
        except YXDOMAIN:
            logger.debug('Failed to resolve "{}"'.format(hostname))
            raise ID4meDNSResolverException('Failed to resolve "{}"'.format(hostname))
        except NoAnswer:
            logger.debug('Failed to find TXT records for "{}"'.format(hostname))
            raise ID4meDNSResolverException('Failed to find TXT records for "{}"'.format(hostname))
        except NoNameservers:
            logger.debug('No nameservers avalaible to dig "{}"'.format(hostname))
            raise ID4meDNSResolverException('No nameservers avalaible to dig "{}"'.format(hostname))
        logger.debug('No suitable TXT DNS entry found for {}'.format(domain))
        raise ID4meDNSResolverException('No suitable TXT DNS entry found for {}'.format(domain))

    def _get_openid_configuration(self, issuer):
        """
        Gets openid configuration of OpenID connect identity
        :param issuer: OpenID connect identity identifier (full URL or FQDN)
        :type issuer: str
        :rtype: dict
        """
        try:
            url = '{}{}{}'.format(
                '' if issuer.startswith('https://') else 'https://',
                issuer,
                '' if issuer.endswith('/') else '/'
            )
            url = urllib.parse.urljoin(url, '.well-known/openid-configuration')
            return get_json_auth(self.networkContext, url)
        except Exception as e:
            logger.debug('Could not get configuration for {} ({})'.format(issuer, e))
            raise ID4meAuthorityConfigurationException('Could not get configuration for {}'.format(issuer))

    # DNSSEC check routine commented out as not used and not validated if correct
    # def _check_dns_sec(self, domain):
    #     try:
    #         domain_authority = self.resolver.query(domain, 'SOA')
    #         response = self.resolver.query(domain_authority, 'NS')
    #         nsname = response.rrset[0]
    #         response = self.resolver.query(nsname, 'A')
    #         nsaddr = response.rrset[0].to_text()
    #         # noinspection PyTypeChecker
    #         request = make_query(domain, 'DNSKEY', want_dnssec=True)
    #         # noinspection PyUnresolvedReferences
    #         response = self.resolver.query.udp(request, nsaddr)
    #         if response.rcode() != 0:
    #             logger.debug('No DNSKEY record found for {}'.format(domain))
    #             raise ID4meDNSSECException('No DNSKEY record found for {}'.format(domain))
    #         else:
    #             answer = response.answer
    #             if len(answer) != 2:
    #                 logger.warning('DNSSEC check failed for {}'.format(domain))
    #                 raise ID4meDNSSECException('DNSSEC check failed for {}'.format(domain))
    #             else:
    #                 name = dns.name.from_text(domain)
    #                 try:
    #                     dns.dnssec.validate(answer[0], answer[1], {name: answer[0]})
    #                     logger.debug('DNS response for "{}" is signed.'.format(domain))
    #                 except dns.dnssec.ValidationFailure:
    #                     logger.warning('DNS response for "{}" is insecure. Trusting it anyway'.format(domain))
    #                     raise ID4meDNSSECException(
    #                         'DNS response for "{}" is insecure. Trusting it anyway'.format(domain))
    #     except Exception:
    #         logger.debug('DNSSEC check failed for {}'.format(domain))
    #         raise ID4meDNSSECException('DNSSEC check failed for {}'.format(domain))

    @staticmethod
    def generate_new_private_keys_set():
        """
        Generates a new paid of RSA keys within JKWSet as JSON string
        :return: JKWSet as JSON string
        :rtype: str
        """
        key = jwk.JWK(generate='RSA', size=2048, kid=str(uuid4()))
        kset = jwk.JWKSet()
        kset.add(key)

        token = jwt.JWT(header={}, claims={}, key=key)
        return kset.export(private_keys=True)

    def _register_identity_authority(self, identity_authority):
        """
        :param identity_authority: Identity Authority identifier
        :type identity_authority: str
        :return: dictionary with registration data
        :rtype: dict
        """
        identity_authority_config = self._get_openid_configuration(identity_authority)
        logger.info('registering with new identity authority ({})'.format(identity_authority))

        request = {
            'redirect_uris': ['{}'.format(self.validateUrl)],
        }

        if self.require_id_token_signing is not None:
            if self.require_id_token_signing:
                if 'id_token_signing_alg_values_supported' in identity_authority_config \
                        and {'RS256', 'RS384', 'RS512'}\
                            .intersection(set(identity_authority_config['id_token_signing_alg_values_supported'])):
                    request['id_token_signed_response_alg'] = \
                        max({'RS256', 'RS384', 'RS512'}\
                            .intersection(set(identity_authority_config['id_token_signing_alg_values_supported'])))
                else:
                    raise ID4meRelyingPartyRegistrationException(
                        'Required signature algorithm for id_token RS256, RS384 or RS512 not supported by Authority')
            else:
                if 'id_token_signing_alg_values_supported' in identity_authority_config \
                        and 'none' in identity_authority_config['id_token_signing_alg_values_supported']:
                    request['id_token_signed_response_alg'] = 'none'
                else:
                    raise ID4meRelyingPartyRegistrationException(
                        'Required signature algorithm for id_token none not supported by Authority')

        if self.require_user_info_signing is not None:
            if self.require_user_info_signing:
                if 'userinfo_signing_alg_values_supported' in identity_authority_config \
                        and {'RS256', 'RS384', 'RS512'}\
                        .intersection(set(identity_authority_config['userinfo_signing_alg_values_supported'])):
                    request['userinfo_signed_response_alg'] = \
                        max({'RS256', 'RS384', 'RS512'}\
                        .intersection(set(identity_authority_config['userinfo_signing_alg_values_supported'])))
                else:
                    raise ID4meRelyingPartyRegistrationException(
                        'Required signature algorithm for user_info RS256, RS384 or RS512 not supported by Authority')
            else:
                if 'userinfo_signing_alg_values_supported' in identity_authority_config \
                        and 'none' in identity_authority_config['userinfo_signing_alg_values_supported']:
                    request['userinfo_signed_response_alg'] = 'none'
                else:
                    raise ID4meRelyingPartyRegistrationException(
                        'Required signature algorithm for user_info none not supported by Authority')

        if self.jwksUrl is not None:
            request['jwks_uri'] = self.jwksUrl
        elif self.private_jwks is not None:
            request['jwks'] = json.loads(self.private_jwks.export(private_keys=False))

        if self.requireencryption or self.requireencryption is None:
            if 'id_token_encryption_alg_values_supported' in identity_authority_config \
                    and 'RSA-OAEP-256' in identity_authority_config['id_token_encryption_alg_values_supported'] \
                    and self.private_jwks is not None:
                request['id_token_encrypted_response_alg'] = 'RSA-OAEP-256'
            elif self.requireencryption:
                raise ID4meRelyingPartyRegistrationException(
                    'Required encryption algorithm for id_token RSA-OAEP-256 not supported by Authority')
            if 'userinfo_encryption_alg_values_supported' in identity_authority_config \
                    and 'RSA-OAEP-256' in identity_authority_config['userinfo_encryption_alg_values_supported'] \
                    and self.private_jwks is not None:
                request['userinfo_encrypted_response_alg'] = 'RSA-OAEP-256'
            elif self.requireencryption:
                raise ID4meRelyingPartyRegistrationException(
                    'Required encryption algorithm for userinfo RSA-OAEP-256 not supported by Authority')

        if self.client_name is not None:
            request['client_name'] = self.client_name
        if self.logoUrl is not None:
            request['logo_uri'] = self.logoUrl
        if self.policyUrl is not None:
            request['policy_uri'] = self.policyUrl
        if self.tosUrl is not None:
            request['tos_uri'] = self.tosUrl

        if self.app_type is not None:
            request['application_type'] = str(self.app_type)

        try:
            registration = json.loads(
                post_json(
                    self.networkContext,
                    identity_authority_config['registration_endpoint'],
                    request, accepted_statuses=[200, 201])
            )
            if 'error' in registration and 'error_description' in registration:
                raise ID4meRelyingPartyRegistrationException(
                    'Error registering Relying Party at {}: {}'.format(identity_authority, registration['error_description']))
            if 'client_id' not in registration or 'client_secret' not in registration:
                raise ID4meRelyingPartyRegistrationException(
                    'client_id or client_secret not returned by the Authority during registration')
        except Exception as e:
            raise ID4meRelyingPartyRegistrationException('Could not register {}: {}'.format(identity_authority, e))
        return registration

    def get_rp_context(self, id4me):
        """
        Makes discovery of ID4me identifier id4me. Performs registration at relevant authority,
        if necessary or recalls a saved authority data via a callback
        :param str id4me: ID4me identifier
        :return: context of ID to use with other flows
        :rtype: ID4meContext
        :raises ID4meRelyingPartyRegistrationException: in case of issues with registration
        :raises ID4meDNSResolverException: in case DNS resolution od identity identifier failed
        """
        identity_authority = self._get_identity_authority(id4me)
        identity_authority_config = self._get_openid_configuration(identity_authority)
        logger.debug('identity_authority = {}'.format(identity_authority))
        registration = None
        # noinspection PyBroadException
        try:
            registration = json.loads(self.get_client_registration(identity_authority))
            # Check if client registration expired
            if 'client_secret_expires_at' in registration \
                and registration['client_secret_expires_at'] != 0 \
                and datetime.datetime.fromtimestamp(registration['client_secret_expires_at']) \
                    - datetime.datetime.utcnow() < datetime.timedelta(minutes=5):
                registration = None
        except Exception:
            # ignore all exceptions (we'll try to re-register as fallback
            pass
        if registration is None:
            if self.register_client_dynamically == False:
                raise ID4meRelyingPartyRegistrationException(
                    "Authority {} not found in store or expired and dynamic registration disabled "
                    "(register_client_dynamically==False)".format(identity_authority))
            if self.save_client_registration is None:
                raise ID4meRelyingPartyRegistrationException(
                    "Authority {} not found in store or expired and registration data save handler missing"
                    "(save_client_registration==None)".format(identity_authority))
            registration = self._register_identity_authority(identity_authority)
            self.save_client_registration(identity_authority, json.dumps(registration))

        context = ID4meContext(id4me=id4me,
                               identity_authority=identity_authority,
                               issuer = identity_authority_config['issuer'])
        return context

    @staticmethod
    def _generate_new_nonce():
        return str(uuid4())

    def get_consent_url(self, context, state=None, claimsrequest=None, prompt=None, usenonce=True, scopes=None):
        """
        :param context: identity context (see: ID4meClient.get_context())
        :type context: ID4meContext
        :param state: state (passed back with validate call)
        :type state: str
        :param claimsrequest: specification of requested claims
        :type claimsrequest: ID4meClaimsRequest
        :param prompt: Open ID Connect prompt value
        :type prompt: OIDCPrompt
        :param usenonce: specify if Nonce shall be used
        :type usenonce: bool
        :param scopes: list of scopes (str or OIDCScope)
        :type scopes: list
        :return: Authorization URL
        :rtype: str
        """
        # TODO: document input parameters
        auth_config = self._get_openid_configuration(context.iau)
        registration = json.loads(self.get_client_registration(context.iau))

        endpoint = '{}'.format(self.validateUrl)
        destination = '{}?response_type=code&client_id={}&redirect_uri={}' \
                      '&login_hint={}'.format(
                            auth_config['authorization_endpoint'],
                            urllib.parse.quote(registration['client_id']),
                            urllib.parse.quote(endpoint),
                            urllib.parse.quote(context.id)
                      )

        if state is not None:
            destination = '{}&state={}'.format(
                destination,
                urllib.parse.quote(state)
            )

        if prompt is not None:
            destination = '{}&prompt={}'.format(
                destination,
                urllib.parse.quote(str(prompt))
            )

        if usenonce:
            context.nonce = self._generate_new_nonce()
            destination = '{}&nonce={}'.format(
                destination,
                urllib.parse.quote(str(context.nonce))
            )
        else:
            context.nonce = None

        scopesfromclaims = set()
        if claimsrequest is not None:
            if auth_config.get('claims_parameter_supported', False):
                claims = json.dumps(stringify_keys(claimsrequest), default=lambda o: o.__dict__)
                destination = '{}&claims={}'.format(
                    destination,
                    urllib.parse.quote(claims)
                )
            elif self.use_scope_if_claims_not_supported:
                # go through all the claims and find matching scope containing the claim
                for requesttype in [getattr(claimsrequest, 'id_token', None),
                                    getattr(claimsrequest, 'userinfo', None)]:
                    if requesttype != None:
                        for claim in requesttype:
                            for scope in OIDCScopeToClaim:
                                if str(claim) in map(str, OIDCScopeToClaim[scope]):
                                    scopesfromclaims.add(str(scope))
                                    break
            else:
                raise ID4meClaimsParameterUnsupportedException('Claims parameter not supported by IdP and downgrade to profiles '
                                                      'not configured with use_scope_if_claims_not_supported')

        # by default adding openid scope
        scopesset = set(['openid'])
        # adding any scopes passed as param
        if scopes is not None:
            scopesset.update(map(str, scopes))
        # adding any scopes coming from downgraded claims
        scopesset.update(scopesfromclaims)
        # generate scope string out of it
        scopestr = ' '.join(sorted(scopesset))

        destination = '{}&scope={}'.format(
            destination,
            urllib.parse.quote(scopestr)
        )

        logger.debug('destination = {}'.format(destination))
        return destination

    def get_idtoken(self, context, code):
        """
        Gets ID token
        :param context: identifier context
        :type context: ID4meContext
        :param code: code returned by the Authority on redirect_url
        :type code: str
        :return: id_token
        :rtype: dict
        """

        auth_config = self._get_openid_configuration(context.iau)
        registration = json.loads(self.get_client_registration(context.iau))
        data = 'grant_type=authorization_code&code={}&redirect_uri={}'.format(
            code, urllib.parse.quote(self.validateUrl))
        try:
            response = json.loads(
                post_data(
                    self.networkContext,
                    auth_config['token_endpoint'],
                    data,
                    basic_auth=(registration['client_id'], registration['client_secret'])
                )
            )
        except Exception as e:
            logger.debug('Failed to get id token from {} for {} ({})'.format(context.iau, context.id, e))
            raise ID4meTokenRequestException(
                'Failed to get id token from {} ({})'.format(context.iau, e))
        if 'access_token' in response and 'token_type' in response and response['token_type'].lower() == 'bearer':
            context.access_token = response['access_token']
            # TODO: [Protocol] access_token is a JWS, not JWE. Too much disclosure?
            # to enable encryption we need different access_tokens for each distributed claims provider
            # (encrypted with their public keys)
            # decoded_token = self._decode_token(context.access_token, context, context.iau, verify_aud=False)
        else:
            logger.debug('Access token missing in authority token response from {} for {}'.format(context.iau, context.id))
            raise ID4meTokenRequestException('Access token missing in authority token response')
        if 'refresh_token' in response:
            context.refresh_token = response['refresh_token']
        if 'id_token' in response:
            payload = self._decode_token(response['id_token'], context, registration, context.iau, TokenDecodeType.IDToken, verify_aud=True)
            context.iss = payload['iss']
            context.sub = payload['sub']
            return payload
        else:
            logger.debug(
                'ID token missing in authority token response from {} for {}'.format(context.iau, context.id))
            raise ID4meTokenRequestException('ID token missing in authority token response')

    def get_user_info(self, context, max_recoursion=3):
        """
        :param context: identifier context
        :type context: ID4meContext
        :param max_recoursion: maximum recoursion level by distributed claims
        :type max_recoursion: int
        :return: user_info
        :rtype dict
        :exception ID4meUserInfoRequestException: thrown on any exception fetching the data
        """
        if context.access_token is None:
            logger.debug(
                'No access token is session. Call id_token() first. From {} for {}'.format(context.iau, context.id))
            raise ID4meUserInfoRequestException('No access token is session. Call id_token() first.')
        # TODO: we need to check access token for expiry and renew with refresh_token if expired (and avail.)
        auth_config = self._get_openid_configuration(context.iau)
        registration = json.loads(self.get_client_registration(context.iau))
        accept = 'application/json+jwt' \
            if ('userinfo_signed_response_alg' in registration
                and registration['userinfo_signed_response_alg'] != 'none')\
            else 'application/json'
        try:
            response, _, ctype = http_request(
                context=self.networkContext,
                method='GET',
                url=auth_config['userinfo_endpoint'],
                bearer=context.access_token,
                accepts= accept
            )
        except Exception as e:
            logger.debug(
                'Failed to get user info from {} for {} ({})'.format(auth_config['userinfo_endpoint'], context.id, e))
            raise ID4meUserInfoRequestException(
                'Failed to get user info from {} ({})'.format(auth_config['userinfo_endpoint'], e))
        user_claims = {
            'iss': context.iss,
            'sub': context.sub
        }
        self._decode_user_info(context, registration, response, ctype,
                               user_claims, context.iss, max_recoursion=max_recoursion)
        return user_claims

    def _get_distributed_claims(self, context, registration, endpoint, access_code, user_claims, leeway, max_recoursion):
        """
        :param context: identifier context
        :type context: ID4meContext
        :param registration: authority registration configuration
        :type registration: dict
        :param endpoint: user info end_point
        :type endpoint: str
        :param access_code: access code
        :type access_code: str
        :param user_claims: result holder (will be updated)
        :type user_claims: dict
        :param leeway: token verification leeway
        :type leeway: datetime.timedelta
        :param max_recoursion: maximum recoursion level by distributed claims
        :type max_recoursion: int
        :rtype: None
        :exception ID4meUserInfoRequestException: thrown on any exception fetching the data
        """
        try:
            logging.debug('Getting distributed claims from: {}'.format(endpoint))
            response, status, ctype = http_request(
                context=self.networkContext,
                url=endpoint,
                method='GET',
                bearer=access_code,
                accepted_statuses=[200]
            )
            # SPEC: [Protocol] seems that distributed claims just come as JWT, not JWE
            # SPEC: [Protocol] need to figure out how client's public keys are to be passed down to agent
            self._decode_user_info(context, registration, response, ctype,
                                   user_claims, None, leeway, max_recoursion)
        except Exception as e:
            logger.debug(
                'Failed to get distributed user info from {} for {} ({})'.format(endpoint, context.id, e))
            raise ID4meUserInfoRequestException(
                'Failed to get distributed user info from {} ({})'.format(endpoint, e))
        return

    def _decode_token(self, token, context, registration, iss, tokentype, leeway=datetime.timedelta(minutes=5),
                      verify_aud=True):
        """
        Decodes OIDC tokens
        :param token: encoded token
        :type token: str
        :param context: identifier context
        :type context: ID4meContext
        :param registration: authority registration
        :type registration: dict
        :param iss: issuer
        :type iss: str
        :param tokentype: type of token (determines verification routines)
        :type tokentype: TokenDecodeType
        :param leeway: token verification leeway
        :type leeway: datetime.timedelta
        :param verify_aud: whether aud field shall be verified
        :type verify_aud: bool
        :return: decoded token
        :rtype: dict
        """
        tokenproc = jwt.JWT()
        tokenproc.leeway = leeway.total_seconds()
        # first deserialize without key to get to the header (and detect type)
        tokenproc.deserialize(token)

        encryptionused = False
        if isinstance(tokenproc.token, jwe.JWE):
            # if it's JWE, decrypt with private key first
            tokenproc.deserialize(token, self.private_jwks)
            encryptionused = True
            token = tokenproc.claims
            tokenproc.deserialize(token)

        if self.requireencryption and not encryptionused:
            logger.debug(
                'Token does not use encryption when required for {}'.format(context.id))
            raise ID4meTokenException('Token does not use encryption when required')

        if iss is None:
            iss = json.loads(tokenproc.token.objects['payload'].decode('utf8'))['iss']
        issuer_config = self._get_openid_configuration(iss)
        keys = self._get_public_keys_set(issuer_config['jwks_uri'])

        try:
            # HACK: we need to check if there is key id in the header (otherwise we need a try all matching keys...)
            # [Agent] clarify why Agent does not set kid as workaround seems clunky
            head = tokenproc.token.jose_header

            if 'typ' in head and head['typ'] != 'JWT':
                logger.debug('Invalid token type for {}'.format(context.id))
                raise ID4meTokenException('Invalid token type')

            if 'alg' not in head:
                logger.debug('Invalid or missing token signature algorithm for {}'.format(context.id))
                raise ID4meTokenException('Invalid or missing token signature algorithm')

            if tokentype == TokenDecodeType.IDToken \
                    and 'id_token_signed_response_alg' in registration \
                    and head['alg'] != registration['id_token_signed_response_alg']:
                logger.debug('Invalid token signature algorithm for {}. Expected: {}, Received: {}'
                             .format(context.id, registration['id_token_signed_response_alg'], head['alg']))
                raise ID4meTokenException('Invalid token signature algorithm. Expected: {0}, Received: {1}'
                    .format(registration['id_token_signed_response_alg'], head['alg']))
            if tokentype == TokenDecodeType.UserInfo \
                    and 'userinfo_signed_response_alg' in registration \
                    and head['alg'] != registration['userinfo_signed_response_alg']:
                logger.debug('Invalid userinfo signature algorithm for {}. Expected: {}, Received: {}'
                             .format(context.id, registration['userinfo_signed_response_alg'], head['alg']))
                raise ID4meTokenException('Invalid userinfo signature algorithm. Expected: {0}, Received: {1}'.format(
                    registration['userinfo_signed_response_alg'], head['alg']))

            if 'kid' not in head and 'alg' in head and head['alg'] != 'none' and head['alg'] in _jws_alg_map:
                success = False
                for k in keys:
                    if (k.get_op_key('verify') is not None) and k.key_type == _jws_alg_map[head['alg']]:
                        try:
                            tokenproc.deserialize(token, k)
                            success = True
                            break
                        except (JWException, RuntimeError, ValueError):
                            # trial and error...
                            pass
                if not success:
                    logger.debug('None of keys is able to verify signature for {}'.format(context.id))
                    raise ID4meTokenException("None of keys is able to verify signature")
            else:
                if head['alg'] == 'none':
                    tokenproc.deserialize(token)
                    tokenproc.header = tokenproc.token.jose_header
                    tokenproc.token.objects['valid'] = True
                    tokenproc.claims = tokenproc.token.payload.decode('utf-8')
                else:
                    tokenproc.deserialize(token, keys)
        except JWException as ex:
            logger.debug('Cannot decode token for {} ({})'.format(context.id, ex))
            raise ID4meTokenException("Cannot decode token: {}".format(ex))

        try:
            payload = json.loads(tokenproc.claims)
        except ValueError as ex:
            logger.debug('Cannot decode claims content for {} ({})'.format(context.id, ex))
            raise ID4meTokenException("Cannot decode claims content: {}".format(ex))

        if 'id4me.identifier' in payload and context.id != payload['id4me.identifier']:
            logger.debug('Identifier mismatch in token for {}'.format(context.id))
            raise ID4meTokenException(
                'Identifier mismatch in token. Requested: {}, Received: {}'.format(context.id,
                                                                                   payload['id4me.identifier']))
        if context.sub is not None and context.sub != payload['sub']:
            logger.debug('Sub mismatch in token for {}'.format(context.id))
            raise ID4meTokenException('sub mismatch in token')
        # ID token specific verifi cation rules
        if tokentype == TokenDecodeType.IDToken:
            if 'iss' not in payload:
                logger.debug('Issuer missing in ID Token for {}'.format(context.id))
                raise ID4meTokenException('Issuer missing in ID Token')
            if payload['iss'] != context.issuer:
                logger.debug('Wrong issuer for ID Token for {}'.format(context.id))
                raise ID4meTokenException('Wrong issuer for ID Token. Expected: {}, Received: {}'.format(context.issuer, payload['iss']))
            if type(payload['aud']) is list and len(payload['aud']) > 1 and 'azp' not in payload:
                logger.debug('Multiple aud in token, but missing azp for {}'.format(context.id))
                raise ID4meTokenException('Multiple aud in token, but missing azp')
            if context.nonce is not None:
                if 'nonce' not in payload:
                    logger.debug('Nonce missing and expected from the context for {}'.format(context.id))
                    raise ID4meTokenException('Nonce missing and expected from the context')
                if payload['nonce'] != context.nonce:
                    logger.debug('Wrong nonce for {}'.format(context.id))
                    raise ID4meTokenException('Wrong nonce. Expected: {}, Received: {}'.format(context.nonce, payload['nonce']))
            if 'nonce' in payload and context.nonce is None:
                logger.debug('Nonce replay detected for {}'.format(context.id))
                raise ID4meTokenException(
                    'Nonce replay detected. Expected: None, Received: {}'.format(payload['nonce']))

        if verify_aud and 'aud' in payload \
                and ((not type(payload['aud']) is list and payload['aud'] != registration['client_id'])
                     or (type(payload['aud']) is list and registration['client_id'] not in payload['aud'])):
            logger.debug('aud mismatch in token for {}'.format(context.id))
            raise ID4meTokenException('aud mismatch in token')
        if 'azp' in payload and payload['azp'] != registration['client_id']:
            logger.debug('azp mismatch in token for {}'.format(context.id))
            raise ID4meTokenException('azp mismatch in token')

        # validation finished
        # if there is nonce in the context and ID_token was decoded - remove nonce
        if tokentype == TokenDecodeType.IDToken:
            context.nonce = None
        return payload

    def _get_public_keys_set(self, jwks_uri):
        try:
            jwks, _, _ = http_request(self.networkContext, method='GET', url=jwks_uri)
            ret = jwk.JWKSet.from_json(jwks)
        except Exception as ex:
            logger.debug('Could not get public keys for {}, {}'.format(jwks_uri, ex))
            raise ID4meAuthorityConfigurationException('Could not get public keys for {}, {}'.format(jwks_uri, ex))
        return ret

    def _decode_user_info(self, context, registration, userinforesponse, content_type, user_claims, iss=None,
                          leeway=datetime.timedelta(minutes=5), max_recoursion=3):
        """
        Decodes user info including traversal to distributed claims provider if needed
        :param context: identifier context
        :type context: ID4meContext
        :param registration: authority registration
        :type registration: dict
        :param userinforesponse: User Info response
        :type userinforesponse: str
        :param content_type: content type string (can contain options as in http header)
        :type content_type: string
        :param user_claims: placeholder for results (claims dictionary)
        :type user_claims: dict
        :param iss: identity issuer, if None will be taken from the token
        :type iss: str
        :param leeway: token verification leeway
        :type leeway: datetime.timedelta
        :param max_recoursion: maximum recoursion level by distributed claims
        :type max_recoursion: int
        """

        mimetype, options = cgi.parse_header(content_type)
        if mimetype in ['application/json+jwt', 'application/jwt', 'application/jws', 'application/jwe']:
            response = self._decode_token(userinforesponse, context, registration, iss, TokenDecodeType.UserInfo, leeway)
        else:
            response = json.loads(userinforesponse)

        # first get the keys from the parent object
        for key in response:
            if key != '_claim_sources' and key != '_claim_names' and key not in user_claims:
                user_claims[key] = response[key]

        #checking distributed claims (if recursion level not exceeded)
        if max_recoursion > 0:
            queried_endpoints = {}
            if '_claim_sources' in response and '_claim_names' in response:
                for claimref in response['_claim_names']:
                    if response['_claim_names'][claimref] in response['_claim_sources'] \
                            and 'access_token' in response['_claim_sources'][response['_claim_names'][claimref]] \
                            and 'endpoint' in response['_claim_sources'][response['_claim_names'][claimref]]:
                        endpoint = response['_claim_sources'][response['_claim_names'][claimref]]['endpoint']
                        access_token = response['_claim_sources'][response['_claim_names'][claimref]]['access_token']
                        if (endpoint, access_token) not in queried_endpoints:
                            self._get_distributed_claims(context, registration, endpoint, access_token, user_claims,
                                                         leeway, max_recoursion - 1)
                            queried_endpoints[(endpoint, access_token)] = True
