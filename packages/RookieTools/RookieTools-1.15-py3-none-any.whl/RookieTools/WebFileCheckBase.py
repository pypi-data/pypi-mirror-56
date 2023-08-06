# -*- coding: utf-8 -*-
# !/usr/bin/env/ python3
"""
WebFile检查基础框架
Author: Rookie
E-mail: hyll8882019@outlook.com
"""

from collections import deque
from threading import Thread
from RookieTools.logger import logger
from RookieTools.ip import is_special_ip
from RookieTools.common import downloader
from RookieTools.CheckBase import CheckBase, abstractmethod


class WebFileCheckBase(CheckBase):
    PluginName = None
    ThreadNumber = 10
    DEBUG = False
    GetOneResult = False

    def __init__(self, url):
        self.url = url
        self.tasks = deque()
        self.result = []
        super(WebFileCheckBase, self).__init__()

    @abstractmethod
    def tasks_init(self):
        pass

    def init_check(self) -> bool:
        resp = downloader(self.url, stream=True, output_error=self.DEBUG)
        if resp is None:
            return False
        try:
            return not is_special_ip(resp.raw._connection.sock.getpeername()[0])
        except AttributeError:
            pass
        except Exception as e:
            logger.exception(e)
            return False
        finally:
            resp.close()

    @abstractmethod
    def check(self, path):
        pass

    def work_in(self):
        while True:
            try:
                path = self.tasks.popleft()
            except IndexError:
                break

            if self.check(path) and self.result:
                with self.file_lock:
                    self.pipe(self.result)

                if self.GetOneResult:
                    self.clean_tasks()

    def run(self):
        status = self.init_check()
        logger.info('% -40s %s %s' % (self.url, self.PluginName, '初始化检查正常' if status else '初始化检查不正常'))
        if status:
            self.tasks_init()
            thds = [Thread(target=self.work_in) for _ in range(self.ThreadNumber)]
            [thd.start() for thd in thds]
            [thd.join() for thd in thds]

    @abstractmethod
    def pipe(self, result):
        pass

    def clean_tasks(self):
        with self.task_lock:
            if len(self.tasks):
                logger.info('% -40s正在清空任务队列. 请稍后....' % self.url)

            self.tasks.clear()
