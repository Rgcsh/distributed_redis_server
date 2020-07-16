# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/9/17 10:18'
"""


class BaseConfig(object):
    """配置基类"""
    DEBUG = False

    # 随机秘钥
    SECRET_KEY = 'ieoqpfjewiofu9eofjpes039ew[d[e0dks0erg93,u94pqm2i0[v-rt5-9302,dw-x-01%h&b=jfx$x01'

    # 是否启用跨域
    CORS_ENABLE = False

    # 是否打印API的Log (LogMiddleWare 使用)
    API_LOG = True

    # redis
    REDIS_URL = 'redis://:password@host:port/db'

    # 日志
    LOGGING_INFO_FILE = None
    LOGGING_ERROR_FILE = None
    BASE_LOGGING = {
        'version': 1,
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'info_file', 'error_file'],
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s | %(levelname)s | %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default',
            },
            'info_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_INFO_FILE,
                'maxBytes': (1 * 1024 * 1024),
                'backupCount': 10,
                'encoding': 'utf8',
                'level': 'INFO',
                'formatter': 'default',
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_ERROR_FILE,
                'maxBytes': (1 * 1024 * 1024),
                'backupCount': 10,
                'encoding': 'utf8',
                'level': 'ERROR',
                'formatter': 'default',
            },
        },
    }

    def __init__(self):
        if self.LOGGING_INFO_FILE:
            self.BASE_LOGGING['handlers']['info_file']['filename'] = self.LOGGING_INFO_FILE

        if self.LOGGING_ERROR_FILE:
            self.BASE_LOGGING['handlers']['error_file']['filename'] = self.LOGGING_ERROR_FILE
