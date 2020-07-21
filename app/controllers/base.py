# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/9/17 10:18'
"""
import traceback

# pylint:disable=wrong-import-order
import redis
from flask_restful import Api, Resource

from app.core import logger
from app.utils import json_fail
from app.utils.exceptions import PPException


class BaseApi(Api):
    """基类"""

    def handle_error(self, e):
        """ 处理异常
        """
        if isinstance(e, PPException):
            return json_fail(e.code, e.message)

        # 打印错误到控制台 和 日志
        logger.error(traceback.format_exc())
        # redis错误
        if isinstance(e, redis.exceptions.RedisError):
            # 说明redis容量不足
            if 'OOM' in str(e):
                return json_fail(10402)
            return json_fail(10403)

        return json_fail(500)


class BaseController(Resource):
    """基类"""

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument,no-self-use
        """ GET 方法基类
        """
        return json_fail(405)

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument,no-self-use
        """ POST 方法基类
        """
        return json_fail(405)
