# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/9/17 10:18'
"""
import atexit
import logging.config
import os

from app.core import scheduler
from app.utils import get_conf


class Config:
    """配置类"""

    def __init__(self, app):
        self.conf = get_conf()
        self.app = app
        self.init_base_config(app)
        self.init_app(app)

    def init_base_config(self, app):
        """
        初始化 基础配置
        :param app:
        :return:
        """
        # 是否debug
        app.config['DEBUG'] = False
        # 中间件
        app.config['MIDDLEWARE'] = [
            'app.middleware.log.LogMiddleWare',
        ]
        # 是否打印API的Log (LogMiddleWare 使用)
        app.config['API_LOG'] = True
        # 日志
        app.config['LOGGING_INFO_FILE'] = '/tmp/info.log'
        app.config['LOGGING_ERROR_FILE'] = '/tmp/error.log'

        # 随机秘钥
        app.config[
            'SECRET_KEY'] = 'ieoqpfjewiofu04-302=;9eofjpes039ew[d[e0dks0erg93,u94pqm2i0[v-rt5-9302,dw-x-01%h&b=jfx$x01'

        # 前端文件路径
        app.config['FRONT_URL'] = 'upload/tender_manage/'

    @classmethod
    def init_extensions(cls, flask_app):
        """ 配置Flask扩展
        """
        from app import core  # pylint: disable=import-outside-toplevel
        for extension in core.__all__:
            obj = getattr(core, extension)
            if hasattr(obj, 'init_app'):
                obj.init_app(flask_app)
        if os.name == 'nt':
            scheduler.start()
        else:
            cls.safe_start_scheduler(flask_app)

    @classmethod
    def safe_start_scheduler(cls, app):
        """Start APScheduler in multi process mode
        """
        import fcntl
        lock_file = open("run-scheduler.lock", "wb")
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.start()
        except Exception as _:
            pass

        def unlock():
            fcntl.flock(lock_file, fcntl.LOCK_UN)
            lock_file.close()

        atexit.register(unlock)

    def init_app(self, app):
        """ 初始化APP
        """
        self.init_core(app)
        self.init_log(app)
        self.init_redis(app)

    def init_core(self, app):
        """ 初始化Core模块参数
        """
        core = self.conf.get("core", dict())

        # Auto config core info
        for key, value in core.items():
            app.config[key.upper()] = value

    def init_log(self, app):
        """ 初始化Log模块参数
        """
        log = self.conf.get("log", dict())
        for key, value in log.items():
            app.config[key.upper()] = value

        # 配置日志
        base_logging = {
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
                    'filename': app.config['LOGGING_INFO_FILE'],
                    'maxBytes': (1 * 1024 * 1024),
                    'backupCount': 10,
                    'encoding': 'utf8',
                    'level': 'INFO',
                    'formatter': 'default',
                },
                'error_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': app.config['LOGGING_ERROR_FILE'],
                    'maxBytes': (1 * 1024 * 1024),
                    'backupCount': 10,
                    'encoding': 'utf8',
                    'level': 'ERROR',
                    'formatter': 'default',
                },
            },
        }
        logging.config.dictConfig(base_logging)

    def init_redis(self, app):
        """ 初始化Redis模块参数
        """
        rds = self.conf.get("redis", dict())

        password = rds.get("pass")
        if rds.get('pass'):
            app.config["REDIS_URL"] = f"redis://:{password}@{rds['host']}:{rds['port']}/{rds['db']}"
        else:
            app.config["REDIS_URL"] = f"redis://{rds['host']}:{rds['port']}/{rds['db']}"
