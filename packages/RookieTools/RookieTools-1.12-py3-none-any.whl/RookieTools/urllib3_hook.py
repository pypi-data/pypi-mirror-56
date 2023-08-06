# -*- coding: utf-8 -*-
# !/usr/bin/env/ python3
"""
Author: Rookie
E-mail: hyll8882019@outlook.com
"""
from io import BytesIO
from requests.exceptions import ContentDecodingError
from urllib3.response import GzipDecoder, DeflateDecoder
import zlib

_GzipDecoder_decompress = GzipDecoder.decompress
_DeflateDecoder_decompress = DeflateDecoder.decompress


def _gzip_boom_check(self, data):
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


def hook_start():
    GzipDecoder.decompress = _gzip_boom_check
    DeflateDecoder.decompress = deflate_boom_check


def hook_stop():
    GzipDecoder.decompress = _GzipDecoder_decompress
    DeflateDecoder.decompress = _DeflateDecoder_decompress
