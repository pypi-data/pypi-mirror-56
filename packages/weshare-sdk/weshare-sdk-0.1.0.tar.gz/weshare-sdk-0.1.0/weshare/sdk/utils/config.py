#!/usr/bin/python
# -*- coding: utf-8 -*-

import errno
import imp
import os
from os.path import abspath, dirname

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def make_dir(dir_name):
    if dir_name is not None and dir_name != '' and not os.path.isdir(dir_name):
        os.makedirs(dir_name)


class DefaultConfig(dict):
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    DATABASE_URI = "sqlite:////tmp/cdnpush.db"

    ENABLED_CHECKED_METRICS = []

    LOG_FILE = ''
    make_dir(dirname(LOG_FILE))

    # scheduler
    SCHEDULER_EXECUTORS = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1,
        'misfire_grace_time': 600
    }

    REPORT_URLS = []


class Config(dict):
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def config_from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def config_from_py(self, filename):
        d = imp.new_module('config')
        d.__file__ = filename
        try:
            with open(filename) as config_file:
                exec (compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.config_from_object(d)
        return True


config = Config()
config.config_from_object(DefaultConfig())
config.config_from_py(dirname(abspath(dirname(__file__))) + "/conf/production.py")
config.config_from_py("/data/config/auth/prod.py")

if __name__ == '__main__':
    print(config)
