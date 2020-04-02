import logging
import os
import sys
from datetime import datetime


def gen_unique_file_name():
    ct = datetime.now()
    return '{}.{}'.format(ct.strftime("%Y%m%d_%H%M%S"), ct.microsecond // 1000)


LOG_FOLDER = 'logs'
LOGGER_NAME = 'MyLogger'


class Logger(object):
    # __created_std_out = False
    log_file = bytes
    EXCEPTION = 100
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    TEXT = 25
    INFO = 20
    TRACE = 15
    DEBUG = 10
    NOTSET = 0

    def __init__(self, log_folder: str = LOG_FOLDER):
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        self._log = logging.getLogger(LOGGER_NAME)
        self._log.propagate = False
        # create formatter
        formatter = logging.Formatter('%(asctime)-15s [%(levelname)-8s] %(message)s')
        file_name = gen_unique_file_name()
        self.log_file = '{}/MyApp-{}.log'.format(log_folder, file_name)
        # create file handler and set level to debug
        file_channel = logging.FileHandler(filename=self.log_file)
        file_channel.setLevel(logging.DEBUG)
        # add formatter to ch
        file_channel.setFormatter(formatter)
        # add ch to logger
        self._log.addHandler(file_channel)

        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self._log.addHandler(ch)

        logging.addLevelName(self.TRACE, "TRACE")

        self._log.setLevel(self.INFO)
        self._methods_map = {
            self.DEBUG: self._log.debug,
            self.TRACE: self._log.info,
            self.TEXT: self._log.info,
            self.INFO: self._log.info,
            self.WARNING: self._log.warning,
            self.ERROR: self._log.error,
            self.CRITICAL: self._log.critical,
            self.EXCEPTION: self._log.exception,
        }

    def __call__(self, lvl, msg, *args, **kwargs):
        if lvl in self._methods_map:
            self._methods_map[lvl](msg, *args, **kwargs)
        else:
            self._log.log(lvl, msg, *args, **kwargs)

    def set_level(self, level=None):
        if level is None:
            level = self.INFO
        self._log.setLevel(level)


log = Logger()
