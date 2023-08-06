from pprint import pprint
import logging
import time
from contextlib import contextmanager
import traceback
import sys
from urllib.parse import urlencode

from urllib3.filepost import encode_multipart_formdata
from urllib3.util.retry import Retry
from urllib3.util.timeout import Timeout
from urllib3 import exceptions, ProxyManager, make_headers
from  urllib3.contrib import pyopenssl
from urllib3.contrib.socks import SOCKSProxyManager
import urllib3
import OpenSSL.SSL
import certifi

from . import error
from .urllib3_custom import CustomPoolManager

urllib3.disable_warnings(exceptions.InsecureRequestWarning)
pyopenssl.inject_into_urllib3()


class Urllib3Transport(object):
    __slots__ = (
        'urllib3_response',
        'op_started',
        'pools',
    )

    def __init__(self, pools=None):
        if pools is None:
            pools = {}
        self.pools = {}
        self.pools[(None, None, True)] = CustomPoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),
        )
        self.pools[(None, None, False)] = CustomPoolManager()
        self.urllib3_response = None

    def prepare_request(self, req, res):
        pass

    @contextmanager
    def handle_network_error(self, req):
        try:
            yield
        except exceptions.ReadTimeoutError as ex:
            raise error.OperationTimeoutError(str(ex), ex)
        except exceptions.ConnectTimeoutError as ex:
            raise error.ConnectError(str(ex), ex)
        except exceptions.ProtocolError as ex:
            raise error.ConnectError(str(ex), ex)
        except exceptions.SSLError as ex:
            raise error.ConnectError(str(ex), ex)
        except OpenSSL.SSL.Error as ex:
            raise error.ConnectError(str(ex), ex)
        except exceptions.LocationParseError as ex:
            raise error.MalformedResponseError(str(ex), ex)
        except exceptions.LocationValueError as ex:
            raise error.InvalidUrlError(str(ex), ex)
        except exceptions.DecodeError as ex:
            raise error.MalformedResponseError(str(ex), ex)
        except exceptions.InvalidHeader as ex:
            raise error.MalformedResponseError(str(ex), ex)
        except exceptions.ProxyError as ex:
            raise error.ProxyError(str(ex), ex)
        except exceptions.MaxRetryError as ex:
            raise error.TooManyRedirects(str(ex), ex)
        except AttributeError:
            # See https://github.com/urllib3/urllib3/issues/1556
            etype, evalue, tb = sys.exc_info()
            frames = traceback.extract_tb(tb)
            found = False
            for frame in frames:
                if (
                        "if host.startswith('[')" in frame.line
                        and 'connectionpool.py' in frame.filename
                    ):
                    found = True
                    break
            if found:
                raise error.MalformedResponseError('Invalid redirect header')
            else:
                raise
        except UnicodeEncodeError as ex:
            # UnicodeEncodeError is subclass of ValueError
            etype, evalue, tb = sys.exc_info()
            frames = traceback.extract_tb(tb)
            #    self._output(request.encode('ascii'))
            #UnicodeEncodeError: 'ascii' codec can't encode characters
            #in position 15-24: ordinal not in range(128)
            if 'self._output(request.encode' in frames[-1].line:
                raise error.InvalidUrlError(
                    'Non ASCII URL: %s' % req.config.get('url')
                )
            else:
                raise
        except ValueError as ex:
            if 'Invalid IPv6 URL' in str(ex):
                raise error.MalformedResponseError('Invalid redirect header')
            else:
                raise
        except KeyError as ex:
            etype, evalue, tb = sys.exc_info()
            frames = traceback.extract_tb(tb)
            if 'self.key_fn_by_scheme[scheme]' in frames[-1].line:
                raise error.InvalidUrlError(
                    'Unknown URL scheme: %s' % req.config.get('url')
                )
            else:
                raise



    def get_pool(self, req, use_cache=True):
        if req['proxy']:
            if req['proxy_type'] == 'socks5' and req['proxy_auth']:
                proxy_url = '%s://%s@%s' % (
                    req['proxy_type'], req['proxy_auth'], req['proxy']
                )
            else:
                proxy_url = '%s://%s' % (req['proxy_type'], req['proxy'])
            pool_key = (req['proxy_type'], req['proxy'], bool(req['verify']))
            if not use_cache or pool_key not in self.pools:
                if req['proxy_type'] == 'socks5':
                    if req['verify']:
                        pool = SOCKSProxyManager(
                            proxy_url,
                            cert_reqs='CERT_REQUIRED',
                            ca_certs=certifi.where(),
                        )
                    else:
                        pool = SOCKSProxyManager(proxy_url, **opts)
                elif req['proxy_type'] == 'http':
                    if req['proxy_auth']:
                        proxy_headers = make_headers(proxy_basic_auth=req['proxy_auth'])
                    else:
                        proxy_headers = None
                    if req['verify']:
                        pool = ProxyManager(
                            proxy_url,
                            proxy_headers=proxy_headers,
                            cert_reqs='CERT_REQUIRED',
                            ca_certs=certifi.where(),
                        )
                    else:
                        pool = ProxyManager(
                            proxy_url,
                            proxy_headers=proxy_headers,
                        )
                else:
                    raise IowebConfigError(
                        'Invalid value of request option `proxy_type`: %s'
                        % req['proxy_type']
                    )
                if use_cache:
                    self.pools[pool_key] = pool
            else:
                pool = self.pools[pool_key]
        else:
            pool = self.pools[(None, None, bool(req['verify']))]
        return pool

    def request(self, req, res):
        options = {}
        headers = req['headers'] or {}

        req_url = req['url']
        if req_url.endswith('?'):
            req_url = req['url'][:-1]

        #req_url = req['url']
        #if not '://' in req_url:
        #    req_url = 'http://%s' % req_url
        #url_parts = urlsplit(req_url)
        #if url_parts.scheme not in ('http', 'https'):
        #    emsg = 'Unknown scheme [%s]' % url_parts.scheme
        #    # second argument saved as `err.transport_error`
        #    # and used then to generate short code of error
        #    # for statistics
        #    raise error.InvalidUrlError(
        #        emsg, error.InvalidUrlError(emsg),
        #    )

        pool = self.get_pool(
            req,
            use_cache=(not req['close_connection'])
        )

        self.op_started = time.time()
        if req['resolve']:
            if req['proxy']:
                raise error.IowebConfigError(
                    'Request option `resolve` could not be used along option `proxy`'
                )
            for host, ip in req['resolve'].items():
                pool.resolving_cache[host] = ip


        if req['content_encoding']:
            if not any(x.lower() == 'accept-encoding' for x in headers):
                headers['Accept-Encoding'] = req['content_encoding']

        if req['data']:
            if isinstance(req['data'], dict):
                if req['multipart']:
                    body, ctype = encode_multipart_formata(req['data'])
                else:
                    body = urlencode(req['data'])
                    ctype = 'application/x-www-form-urlencoded'
                options['body'] = body
                headers['Content-Type'] = ctype
            elif isinstance(req['data'], bytes):
                options['body'] = req['data']
            elif isinstance(req['data'], str):
                options['body'] = req['data'].encode('utf-8')
            else:
                raise IowebConfigError(
                    'Invalid type of request data option: %s'
                    % type(req['data'])
                )
            headers['Content-Length'] = len(options['body'])

        with self.handle_network_error(req):
            if req['follow_redirect']:
                retry_opts = {
                    'total': req['max_redirects'],
                    'redirect': req['max_redirects'],
                    'raise_on_redirect': True,
                }
            else:
                retry_opts = {
                    'total': False,
                    'redirect': False,
                    'raise_on_redirect': False,
                }
            self.urllib3_response = pool.urlopen(
                req.method(),
                req_url,
                headers=headers,
                # total - set to None to remove this constraint
                # and fall back on other counts. 
                retries=Retry(
                    connect=False,
                    read=False,
                    **retry_opts,
                ),
                timeout=Timeout(
                    connect=req['connect_timeout'],
                    read=req['timeout'],
                ),
                preload_content=False,
                decode_content=req['decode_content'],
                **options
            )

    def read_with_timeout(self, req, res):
        read_limit = req['content_read_limit']
        chunk_size = 10 * 1024
        bytes_read = 0
        while True:
            chunk = self.urllib3_response.read(chunk_size)
            if chunk:
                if read_limit:
                    chunk_limit = min(len(chunk), read_limit - bytes_read)
                else:
                    chunk_limit = len(chunk)
                res._bytes_body.write(chunk[:chunk_limit])
                bytes_read += chunk_limit
                if read_limit and bytes_read >= read_limit:
                    break
            else:
                break
            if time.time() - self.op_started > req['timeout']:
                raise error.OperationTimeoutError(
                    'Timed out while reading response',
                )

    def prepare_response(self, req, res, err, raise_network_error=True):
        try:
            if err:
                res.error = err
            else:
                try:
                    res.headers = self.urllib3_response.headers
                    res.status = self.urllib3_response.status
                    if len(self.urllib3_response.retries.history):
                        res.url = (
                            # redirect_location might be None
                            # if network errors happened during
                            # processing redirect
                            self.urllib3_response.retries.history[-1].redirect_location
                            or
                            self.urllib3_response.retries.history[-1].url
                        )
                    else:
                        res.url = req['url']

                    if hasattr(self.urllib3_response._connection.sock, 'connection'):
                        res.cert = (
                            self.urllib3_response._connection.sock.connection
                            .get_peer_cert_chain()
                        )

                    with self.handle_network_error(req):
                        self.read_with_timeout(req, res)
                except error.NetworkError as ex:
                    if raise_network_error:
                        raise
                    else:
                        res.error = err
        finally:
            if self.urllib3_response:
                #if req['close_connection']:
                #    self.urllib3_response._connection.close()
                self.urllib3_response.release_conn()
