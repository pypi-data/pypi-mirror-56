# -*- coding: utf-8 -*-
# !/usr/bin/env/ python3
"""
Author: Rookie
E-mail: hyll8882019@outlook.com
"""
from abc import ABC, abstractmethod
from RookieTools.logger import logger
from threading import Lock
import logging


class CheckBase(ABC):
    PluginName = None
    ThreadNumber = 10
    DEBUG = False

    def __init__(self, *args, **kwargs):
        logger.setLevel(logging.DEBUG if self.DEBUG else logging.INFO)
        self.lock = Lock()
        self.file_lock = Lock()
        self.task_lock = Lock()
        self.run()

    @abstractmethod
    def tasks_init(self):
        pass

    @abstractmethod
    def init_check(self) -> bool:
        pass

    @abstractmethod
    def check(self, *args, **kwargs):
        pass

    @abstractmethod
    def work_in(self, *args, **kwargs):
        pass

    def run(self):
        pass

    @abstractmethod
    def pipe(self, result):
        pass

    @abstractmethod
    def clean_tasks(self):
        pass
