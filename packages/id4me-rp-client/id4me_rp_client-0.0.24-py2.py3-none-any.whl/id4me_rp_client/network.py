__author__ = "Pawel Kowalik"
__copyright__ = "Copyright 2018, 1&1 IONOS SE"
__credits__ = ["Andreea Dima", "Marc Laue"]
__license__ = "MIT"
__maintainer__ = "Pawel Kowalik"
__email__ = "pawel-kow@users.noreply.github.com"
__status__ = "Beta"

import base64
import json
import logging
import re
import ssl

from six.moves import http_client as client
from six.moves import urllib

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)


class NetworkContext:
    def __init__(self, proxy_host=None, proxy_port=None, nameservers=None, max_bytes=None, timeout=None):
        """

        :param proxy_host: http(s) proxy host
        :type proxy_host: str
        :param proxy_port: http(s) proxy port
        :type proxy_port: int
        :param nameservers: list of used nameservers
        :type nameservers: list
        :param max_bytes: maximum downloaded length in bytes
        :type max_bytes: int
        :param timeout: connection timeout
        :type timeout: int
        """
        self.proxyPort = proxy_port
        self.proxyHost = proxy_host
        self.nameservers = nameservers
        self.maxbytes = max_bytes
        self.timeout = timeout


def http_request(context, method, url, body=None, basic_auth=None, bearer=None, content_type=None,
                 accepts=None, cache_control=None, accepted_statuses=None, max_bytes=None):
    """

    :param context: Network context
    :type context: NetworkContext
    :param method: str
    :param url: str
    :param body: str
    :param basic_auth: str
    :param bearer: str
    :param content_type: str
    :param accepts: str
    :param cache_control: str
    :param accepted_statuses: list(str)
        list statuses which do not rise exception
    :param max_bytes: int
    :return: tuple (Content, http code, content-type)
    :rtype: tuple (string, int, string)
    """
    if accepted_statuses is None:
        accepted_statuses = [200]

    ret, status, ctype = _http_request_raw(context, method, url, body, basic_auth,
                                    bearer, content_type, accepts, cache_control,
                                    max_bytes)

    if status not in accepted_statuses:
        logger.debug('Failed to query {}: {}\n\r{}'.format(url, status, ret))
        raise Exception('Failed to read from {}. HTTP code: {}, content: {}'.format(url, status, ret))
    return ret.decode('utf-8'), status, ctype


def _http_request_raw(context, method, url, body=None, basic_auth=None, bearer=None, content_type=None,
                      accepts=None, cache_control=None, max_bytes=None):
    """

    :param context: Network context
    :type context: NetworkContext
    :param method: str
    :param url: str
    :param body: str
    :param basic_auth: str
    :param bearer: str
    :param content_type: str
    :param accepts: str
    :param cache_control: str
    :param max_bytes: int
    :return: tuple (Content, http code, content-type)
    :rtype: tuple (string, int, string)
    """

    connection = None
    url_parts = re.match('(?i)(https?)://([^:/]+(?::\d+)?)(/.*)?', url)
    if url_parts is None:
        raise Exception('Not valid URL requested: {}'.format(url))
    protocol = url_parts.group(1).lower()
    host = url_parts.group(2)
    path = url_parts.group(3)
    logger.debug('method = {} protocol = {}, host = {}, path = {}'.format(method, protocol, host, path))
    try:
        if protocol == 'http':
            if context.proxyHost is not None and context.proxyPort is not None:
                logger.debug('using proxy {}:{}'.format(context.proxyHost, context.proxyPort))
                connection = client.HTTPConnection(context.proxyHost, context.proxyPort)
                connection.set_tunnel(host)
            else:
                connection = client.HTTPConnection(host)
        else:
            # noinspection PyProtectedMember
            ssl_context = ssl._create_unverified_context()
            if context.proxyHost is not None and context.proxyPort is not None:
                logger.debug('using proxy {}:{}'.format(context.proxyHost, context.proxyPort))
                connection = client.HTTPSConnection(context.proxyHost, context.proxyPort, context=ssl_context)
                connection.set_tunnel(host)
            else:
                connection = client.HTTPSConnection(host, context=ssl_context)

        # setting timeout to 5s to prevent connection stall DOS
        connection.timeout = context.timeout if context.timeout is not None else 5

        header = dict()
        if basic_auth is not None:
            user, password = basic_auth
            head = ':'.join([user, password]).encode()
            header['Authorization'] = ' '.join(['Basic', base64.b64encode(head).decode()])
        if bearer is not None:
            header['Authorization'] = ' '.join(['Bearer', bearer])
        if content_type is not None:
            header['Content-Type'] = content_type
        if accepts is not None:
            header['Accept'] = accepts
        if cache_control is not None:
            header['Cache-Control'] = cache_control
        connection.request(method, path, body, header)
        response = connection.getresponse()

        maxb = max_bytes if max_bytes is not None else context.maxbytes

        ret = response.read(amt=maxb)

        if maxb and len(ret) >= maxb:
             raise Exception('Failed to read from {}. Maximum content length of {} exceeded ({})'.format(
                 url, maxb, response.length))
        if response.status in [301,302] and method == 'GET':
            loc = response.getheader('Location')
            redirurl = urllib.parse.urljoin(url, loc)
            return _http_request_raw(context, method, redirurl, body, basic_auth, bearer, content_type,
                                     accepts, cache_control, max_bytes)
        return ret, response.status, response.getheader('Content-Type', None)
    finally:
        if connection is not None:
            connection.close()

def post_data(context, url, data, basic_auth=None, bearer=None, accepted_statuses=None, max_bytes=None):
    """

    :type context: NetworkContext
    :param context: network configuration
    :param url: str
    :param data: str
    :param basic_auth: str
    :param bearer: str
    :param accepted_statuses: list(str)
        list statuses which do not rise exception
    :return:
    """
    if accepted_statuses is None:
        accepted_statuses = [200]
    response, status, _ = http_request(context=context, method='POST', url=url, body=data, basic_auth=basic_auth,
                                    bearer=bearer, content_type='application/x-www-form-urlencoded',
                                    accepted_statuses=accepted_statuses, max_bytes=max_bytes)
    return response


def post_json(context, url, content, basic_auth=None, bearer=None, accepted_statuses=None, max_bytes=None):
    """

    :type context: NetworkContext
    :param context: network configuration
    :param url: str
    :param content: str
    :param basic_auth: str
    :param bearer: str
    :param accepted_statuses: list(str)
        list statuses which do not rise exception
    :return:
    """
    if accepted_statuses is None:
        accepted_statuses = [200]
    response, status, _ = http_request(
        context=context, method='POST', url=url, body=json.dumps(content),
        basic_auth=basic_auth, bearer=bearer, content_type='application/json',
        accepted_statuses=accepted_statuses, max_bytes=max_bytes)
    return response

def get_json_auth(context, url, basic_auth=None, bearer=None, accepted_statuses=None, max_bytes=None):
    """

    :param context: NetworkContext
    :param url: str
    :param basic_auth: str
    :param bearer: str
    :return:
    """
    response, status, _ = http_request(
        context=context,
        method='GET',
        url=url,
        basic_auth=basic_auth,
        bearer=bearer,
        accepted_statuses=accepted_statuses,
        max_bytes=max_bytes)
    return json.loads(response)
