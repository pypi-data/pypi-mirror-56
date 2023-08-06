#! /usr/bin/python
# -*- coding: utf-8 -*-

import errno
import os
import platform
import sys
import time
from os.path import dirname


class DaemonHelper:
    def __init__(self, pid_file):
        self.pid_file = pid_file
        self.exit_flag = False

    def enter_daemon(self):
        try:
            if os.fork() > 0:
                sys.exit(0)  # exit farther

            print("start a daemon mode.")

            os.chdir('/')
            os.setsid()
            os.umask(0o033)

            if os.fork() > 0:
                sys.exit(0)

            # redirect standard i/o to /dev/null
            null_file = open('/dev/null', 'a+')
            os.dup2(null_file.fileno(), sys.stdin.fileno())
            os.dup2(null_file.fileno(), sys.stdout.fileno())
            os.dup2(null_file.fileno(), sys.stderr.fileno())

            self.update_pid_file()
            return True
        except (AttributeError, OSError) as e:
            print("fork failed. the os doesn't support daemon mode.")
            sys.exit(1)

    # signal handlers to handle the linux signal
    @staticmethod
    def _manager_signal_handler(self, signum, frame):
        import signal
        _quit_signals = (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT)
        if signum in _quit_signals:
            self.exit_flag = True

    @staticmethod
    def install_signal_handlers():
        import signal
        signal.signal(signal.SIGINT, DaemonHelper._manager_signal_handler)
        signal.signal(signal.SIGTERM, DaemonHelper._manager_signal_handler)
        signal.signal(signal.SIGQUIT, DaemonHelper._manager_signal_handler)
        signal.signal(signal.SIGHUP, DaemonHelper._manager_signal_handler)

    def is_running(self):
        pid = self.get_running_pid()
        if pid == -1:
            return False
        else:
            return DaemonHelper.is_pid_running(pid)

    @staticmethod
    def is_pid_running(pid):
        return False if platform.system() == 'Windows' else DaemonHelper._is_pid_running_on_unix(pid)

    @staticmethod
    def _is_pid_running_on_unix(pid):
        return pid_exists(pid)

    def get_running_pid(self):
        pid = -1
        if os.path.exists(self.pid_file):
            try:
                with open(self.pid_file) as f:
                    pid = int(f.readline().strip())
            except (AttributeError, OSError) as e:
                pass
        return pid

    def update_pid_file(self):
        with open(self.pid_file, 'w') as f:
            f.write("%s" % os.getpid() + "\n")

    def invalidate_pid_file(self):
        with open(self.pid_file, 'w') as f:
            f.write("%s" % -1 + "\n")

    def stop(self):
        pid = self.get_running_pid()
        if pid != -1:
            os.kill(pid, 15)

            count_time(10, pid)

            if pid_exists(pid):
                os.kill(pid, 9)
                sys.stdout.write("timeout...killed\n")
                sys.stdout.flush()
            else:
                sys.stdout.write("daemon stopped\n")
                sys.stdout.flush()

            self.invalidate_pid_file()


def make_dir(dir_name):
    if dir_name is not None and dir_name != '' and not os.path.isdir(dir_name):
        os.makedirs(dir_name)


def create_daemon(pid_file='/data/var/mysql3306/heartbeat.pid'):
    make_dir(dirname(pid_file))
    return DaemonHelper(pid_file)


def count_time(sleep, pid):
    sys.stdout.write('stopping daemon...')
    sys.stdout.flush()
    while sleep > 0:
        if not pid_exists(pid):
            return

        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)
        sleep -= 1


def pid_exists(pid):
    if pid < 0:
        return False

    if pid == 0:
        raise ValueError('invalid PID 0')

    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            return False
        elif err.errno == errno.EPERM:
            return True
        else:
            raise
    else:
        return True
