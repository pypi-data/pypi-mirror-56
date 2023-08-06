# -*- coding: utf-8 -*-

import logging.config
import os
import sys

logger = logging.getLogger(__name__)


def app_path():
    # print(hasattr(sys, 'frozen'))
    # print(os.path.dirname(sys.executable))
    # print(os.path.dirname(os.path.abspath("")))
    # print(os.path.dirname(os.path.abspath(".")))
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)
    # return os.path.dirname(os.path.abspath("log/"))
    return os.path.dirname(os.path.abspath(".."))


rootdir = app_path()

# print(rootdir)
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': rootdir + '/log/logging.log',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'timedfile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': rootdir + '/log/logging.log',
            'level': 'DEBUG',
            'formatter': 'simple',
            'interval': 1,
            'backupCount': 30,
            'when': 'D',
            'encoding': 'utf8'
        },
        # 其他的 handler
    },
    'loggers': {
        'monetSpider': {
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console', 'timedfile'],
        'level': "INFO",
        'propagate': False
    }
}


def initLogger():
    logging.config.dictConfig(DEFAULT_LOGGING)
