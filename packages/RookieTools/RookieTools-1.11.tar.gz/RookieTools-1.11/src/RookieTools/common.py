# -*- coding: utf-8 -*-
# !/usr/bin/env/ python3
"""
通用爆破
Author: Rookie
E-mail: hyll8882019@outlook.com
"""

import re
import zlib
import time
import chardet
import requests
import logging
import socket
from requests import session
from io import BytesIO
from requests.exceptions import ContentDecodingError
from urllib3.response import GzipDecoder, DeflateDecoder

g_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.87 Safari/537.36',
    'Connection': 'close'
}
__session = session()

logger = logging.getLogger('Codes')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.INFO)

is_url = lambda x: x.startswith('http://') or x.startswith('https://')


def _set_headers(is_session, **kwargs):
    headers = kwargs.get('headers')
    if not headers:
        headers = g_headers
    else:
        for key in ['User-Agent', 'Connection']:
            if key not in headers:
                headers[key] = g_headers[key]

    if is_session:
        headers['Connection'] = 'Keep-alive'
    return headers


def gzip_boom_check(self, data):
    if not hasattr(self, 'total'):
        self.total = 0
    if not hasattr(self, 'gzip'):
        self.gzip = zlib.decompressobj(15 + 16)

    with BytesIO(data) as f:
        while True:
            buf = self.gzip.unconsumed_tail
            if not buf:
                buf = f.read(1024)
                if not buf:
                    break
            got = self.gzip.decompress(buf, 4096)
            if not got:
                break
            self.total += len(got)

        if self.total > ((1 << 30) / 10):
            raise ContentDecodingError('is GzipBoom data size: %0.2fG' % (self.total / (1 << 30)))
        else:
            return _GzipDecoder_decompress(self, data)


def deflate_boom_check(self, data):
    # TODO: 尚未实现deflate压缩炸弹检查
    return _DeflateDecoder_decompress(self, data)
    # with BytesIO(data) as f:
    #     while True:
    #         buf = self.gzip.unconsumed_tail
    #         if not buf:
    #             buf = f.read(4096)
    #             if not buf:
    #                 break
    #         got = self.gzip.decompress(buf)
    #         if not got:
    #             break
    #         self.total += len(got)
    #         print(self.total)
    #     if self.total > ((1 << 30) / 2):
    #         raise ContentDecodingError('is GzipBoom data size: %0.2fG' % (self.total / (1 << 30)))
    #     else:
    #         return _DeflateDecoder_decompress(self, data)
    # _DeflateDecoder_decompress(self, data)


_GzipDecoder_decompress = GzipDecoder.decompress
GzipDecoder.decompress = gzip_boom_check

_DeflateDecoder_decompress = DeflateDecoder.decompress
DeflateDecoder.decompress = deflate_boom_check


def init_boom_check(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@init_boom_check
def downloader(url: str, is_session: bool = False, **kwargs):
    if not url:
        return None

    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url

    if 'timeout' not in kwargs:
        kwargs['timeout'] = 30

    res_data = {'url': url, 'headers': _set_headers(is_session, **kwargs), **kwargs}
    try:
        if 'data' in kwargs:
            if is_session:
                return requests.post(**res_data)
            else:
                return __session.post(**res_data)

        if is_session:
            return requests.get(**res_data)
        else:
            return __session.get(**res_data)
    except ContentDecodingError as e:
        try:
            info = re.findall('is G?zipBoom data size: .*?G', str(e.args))[0]
        except IndexError:
            info = e.args

        logger.warning('% -40s %s' % (url, info))
    except MemoryError:
        logger.warning('内存使用限制为1G: %s, 超过. 可能为压缩包炸弹' % url)
    except requests.exceptions.TooManyRedirects:
        logger.warning('重定向次数过多: %s' % url)
    except requests.exceptions.RequestException:
        # logger.error('network error: %s, %s' % (url, e.args))
        pass
    except Exception as e:
        logger.error('network error: %s, %s' % (url, e.args))
        logger.exception(e)

    return None


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
            return chardet.detect(resp.content)['encoding']
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
    try:
        host = socket.gethostbyname(domain)
    except Exception as e:
        logger.warning('host to ip error: %s' % e.args)
        return None

    logger.info('Get Host: %s' % host)
    return host


def is_open_port(host: str, port: int) -> bool:
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


if __name__ == '__main__':
    _resp = downloader('http://127.0.0.1')
    if not _resp:
        exit()
    print(html_decode(_resp))
