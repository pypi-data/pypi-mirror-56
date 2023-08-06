# -*- coding: utf-8 -*-
# !/usr/bin/env/ python3
"""
Author: Rookie
E-mail: hyll8882019@outlook.com
"""
import logging
import tldextract
from collections import deque
from threading import Lock, Thread
from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod
from RookieTools.common import logger, show_run_time, is_url
from urllib.parse import urlparse


class PassWordCheckBase(ABC):
    PluginName = None
    ThreadNumber = 10
    DEBUG = False

    def __init__(self, target: str):
        logger.setLevel(logging.DEBUG if self.DEBUG else logging.INFO)
        self.url = target
        self.result = None
        self.lock = Lock()
        self.__file_lock = Lock()
        self.__task_lock = Lock()
        self.username_task = deque()
        self.password_task = deque()
        self.__password_task = None
        self.run()

    @abstractmethod
    def init_check(self) -> bool:
        pass

    @abstractmethod
    def tasks_init(self):
        pass

    @abstractmethod
    def check(self, username, password) -> bool:
        pass

    def init_domain_pass(self, is_user: bool = True, is_pass: bool = True):
        if not is_url(self.url.lower()):
            self.url = 'http://' + self.url.lower()
        try:
            domain = urlparse(self.url).netloc
        except ValueError:
            logger.warning('parse url fail: %s' % self.url)
            return

        tld = tldextract.extract(domain)
        sub_domain = tld.subdomain
        if '.' in sub_domain:
            sub_domain = sub_domain.split('.')
        else:
            sub_domain = [sub_domain, ]
        domains = [
            '%s' % tld.domain,
            '%s%s' % (tld.domain, tld.suffix), '%s%s%s' % (''.join(sub_domain), tld.domain, tld.suffix),
            '%s_%s' % (tld.domain, tld.suffix), '%s_%s_%s' % ('_'.join(sub_domain), tld.domain, tld.suffix),
            '%s.%s' % (tld.domain, tld.suffix), '%s.%s.%s' % ('.'.join(sub_domain), tld.domain, tld.suffix)
        ]
        if is_user:
            [self.username_task.append(i) for i in domains]

        if is_pass:
            [self.password_task.append(i) for i in domains]

    def __clean_tasks(self):
        with self.__task_lock:
            if len(self.password_task) or len(self.username_task):
                logger.info('% -40s正在清空任务队列. 请稍后....' % self.url)

            self.username_task.clear()
            self.password_task.clear()
            if self.__password_task:
                self.__password_task.clear()

    def is_exist(self):
        return self.result is not None

    def work_in(self, username: str):
        while True:
            try:
                password = self.__password_task.popleft()
            except IndexError:
                break

            if self.check(username, password):
                if self.result:
                    with self.__file_lock:
                        self.pipe(self.result)

                self.__clean_tasks()

    @abstractmethod
    def pipe(self, result):
        pass

    @show_run_time('PasswordCheck')
    def run(self):
        status = self.init_check()
        logger.info('% -40s %s %s' % (self.url, '存在' if status else '不存在', self.PluginName))
        if status:
            self.tasks_init()
            while True:
                try:
                    username = self.username_task.popleft()
                except IndexError:
                    break
                self.__password_task = self.password_task.copy()

                thds = [Thread(target=self.work_in, args=(username,)) for _ in range(self.ThreadNumber)]
                [thd.start() for thd in thds]
                [thd.join() for thd in thds]


def pool(targets: list, obj: PassWordCheckBase):
    _pool = ThreadPoolExecutor()
    _pool.map(obj, targets)
    _pool.shutdown()
