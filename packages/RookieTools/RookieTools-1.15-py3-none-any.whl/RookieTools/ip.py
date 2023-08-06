# -*- coding: utf-8 -*-
# !/usr/bin/env/ python3
"""
Author: Rookie
E-mail: hyll8882019@outlook.com
"""
import IPy
import socket
from RookieTools.logger import logger

SpecialIp = [
    '127.0.0.0/8', '10.0.0.0/8', '172.16.0.0-172.31.255.255', '169.254.0.0-169.254.255.255',
    '192.168.0.0-192.168.255.255', '224.0.0.0-224.0.0.255',
    '239.0.0.0-239.255.255.255', '::1/128', 'FC00::/7', 'FF00::/8', 'FE80::/10', 'FE80::/10',
    ['0.0.0.0', '0.255.255.255', '255.255.255.255']
]


def is_special_ip(ip: str, ips: list = None) -> bool:
    if not ips:
        ips = SpecialIp

    def is_array(x: (str, list)) -> bool:
        return ip in x if isinstance(x, list) else ip in IPy.IP(x)

    for i in ips:
        if is_array(i):
            logger.warning('特殊IP地址: %s' % ip)
            return True
    return False


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
