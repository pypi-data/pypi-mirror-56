#! /usr/bin/python
# -*- coding: utf8 -*-

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from os.path import isdir, dirname

from config import config

LOGFILE = "/data/log/openvpn/userauth.log"


def create_logger(log_file=None, name=None):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(process)s-%(threadName)s %(filename)s %(lineno)d: %(message)s')

    log_file = LOGFILE if not log_file else log_file
    log_file_dir = os.path.dirname(log_file)
    if not os.path.exists(log_file_dir):
        os.makedirs(log_file_dir, 0755)

    ch = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=7)
    # ch = RotatingFileHandler(LOGFILE, maxBytes=5 * 1024 * 104, backupCount=10, encoding='utf-8')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    cs = logging.StreamHandler()
    cs.setFormatter(formatter)
    log.addHandler(cs)
    return log


def get_logger(log_file=None, name=None):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)

    log_file = config['LOG_FILE'] if not log_file else log_file
    if not isdir(dirname(log_file)):
        os.makedirs(dirname(log_file))

    th = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=7)
    th.setFormatter(formatter)
    log.addHandler(th)

    return log


# logger = get_logger()

if __name__ == '__main__':
    print("start logger ...")
    aa = create_logger('/data/aa.log', 'aa')
    bb = create_logger('/data/bb.log', 'bb')
    print aa
    print bb
