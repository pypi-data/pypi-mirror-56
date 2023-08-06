# -*- coding: utf-8 -*-
# !/usr/bin/env/ python3
"""
Author: Rookie
E-mail: hyll8882019@outlook.com
"""
import re
import time
import requests
import socket
import warnings
from concurrent.futures.thread import ThreadPoolExecutor
from requests.exceptions import ContentDecodingError
from RookieTools.urllib3_hook import hook_start
from RookieTools.logger import logger

hook_start()

g_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.87 Safari/537.36',
    'Connection': 'close'
}


def is_url(url: str) -> bool:
    return url.startswith('http://') or url.startswith('https://')


def _is_use_session(x: bool, y: dict):
    return True if x or y.get('stream', False) else False


def _init_downloader(url, is_session: bool = False, **kwargs):
    if not kwargs.get('headers'):
        kwargs['headers'] = g_headers
    else:
        for key in ['User-Agent', 'Connection']:
            if key not in kwargs['headers']:
                kwargs['headers'][key] = g_headers[key]

    if _is_use_session(is_session, kwargs):
        kwargs['headers']['Connection'] = 'Keep-alive'
    if not url:
        return None

    if not is_url(url):
        url = 'http://' + url

    if 'timeout' not in kwargs:
        kwargs['timeout'] = 30

    return {'url': url, **kwargs}


def _downloader_runtime_check(func):
    def wrapper(url, *args, **kwargs):
        output_error = kwargs.pop('output_error', False)
        try:
            return func(url, *args, **kwargs)
        except ContentDecodingError as e:
            if output_error:
                logger.warning('% -40s %s' % (url, re.findall('is G?zipBoom data size: .*?G', str(e.args))[0]))
        except requests.exceptions.RequestException as e:
            if output_error:
                logger.error('network error: %s, %s' % (url, e.args))
        except Exception as e:
            if output_error:
                logger.error('network error: %s, %s' % (url, e.args))
                logger.exception(e)
        return None

    return wrapper


@_downloader_runtime_check
def downloader(url: str, is_session: bool = False, is_head: bool = False, **kwargs):
    def _send(func):
        if _is_use_session(is_session, kwargs):
            return eval('requests.session().%s' % func)(**res_data)
        else:
            return eval('requests.%s' % func)(**res_data)

    res_data = _init_downloader(url, is_session, **kwargs)

    if is_head:
        return _send('head')

    if 'data' in kwargs:
        return _send('post')

    return _send('get')


def get_charset(resp) -> (str, None):
    if resp is None:
        return

    try:
        _charset = re.findall('charset=[\'" ]*([a-zA-Z0-9-]+)[\'"/> ]*', resp.headers.get('Content-Type'))[0]
        _charset = _charset.lower()
    except IndexError:
        _charset = ''

    try:
        charset = re.findall('charset=[\'" ]*([a-zA-Z0-9-]+)[\'"/> ]*', resp.text)[0]
        charset = charset.strip()
    except IndexError as e:
        try:
            return resp.apparent_encoding
        except Exception as e:
            # logger.exception(e)
            logger.warning('get % -40s charset fail' % resp.url)
            return None

    if _charset == charset or not _charset:
        logger.debug('url: %s, charset: %s' % (resp.url, charset))
        return charset
    else:
        # logger.warning('html page charset difference: url: %s, response charset: %s, html page charset: %s' %
        #                (response.url, charset, _charset))
        return _charset, charset


def html_decode(resp):
    if not resp:
        return None

    charset = get_charset(resp)
    if isinstance(charset, str):
        try:
            return resp.content.decode(charset)
        except (UnicodeDecodeError, LookupError):
            logger.warning('UnicodeDecodeError % -40s' % resp.url)
            return None
    elif isinstance(charset, tuple):
        for i in charset:
            try:
                return resp.content.decode(i)
            except (UnicodeDecodeError, LookupError):
                continue
        logger.warning('UnicodeDecodeError % -40s' % resp.url)
        return None
    else:
        logger.warning('UnicodeDecodeError % -40s' % resp.url)
        return None


def show_run_time(name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            start = time.time()
            result = func(self, *args, **kwargs)
            end = time.time()
            logger.info('task time consuming: %s % -40s %0.2fs %s' % (
                name, self.url, end - start, 'success' if self.is_exist() else 'fail'))
            return result

        return wrapper

    return decorator


def host2ip(domain):
    warnings.warn("RookieTools.common.host2ip is deprecated since RookieTools 2.0."
                  "Use RookieTools.host2ip instead.", DeprecationWarning, stacklevel=2)
    try:
        host = socket.gethostbyname(domain)
    except Exception as e:
        logger.warning('host to ip error: %s' % e.args)
        return None

    logger.info('Get Host: %s' % host)
    return host


def is_open_port(host: str, port: int) -> bool:
    warnings.warn("RookieTools.common.is_open_port is deprecated since RookieTools 2.0."
                  "Use RookieTools.is_open_port instead.", DeprecationWarning, stacklevel=2)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        s.close()
        logger.info('port: %s %d open' % (host, port))
        return True
    except Exception as e:
        logger.info('port: %s %d close' % (host, port))
        return False


def pool(targets: list, obj: object):
    _pool = ThreadPoolExecutor()
    _pool.map(obj, targets)
    _pool.shutdown()


if __name__ == '__main__':
    downloader('http://127.0.0.1', output_error=True)
