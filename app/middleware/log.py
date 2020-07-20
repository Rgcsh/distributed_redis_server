# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/6/27 10:18'
"""
import json

from flask import request
from app.core import logger

from .base import BaseMiddleWare


class LogMiddleWare(BaseMiddleWare):
    """记录日志的中间件"""

    @staticmethod
    def before_request():
        # 获取请求参数
        request_params = request.args.to_dict()
        if request.method == "POST":
            request_params = request.form.to_dict()
        if not request_params:
            try:
                request_params = request.json
            except Exception:
                request_params = {}

        log_info = {
            "host": request.host_url,
            "path": request.path,
            "method": request.method,
            "request": {
                "header": dict(request.headers),
                "params": request_params
            }
        }
        logger.info(log_info)

    @staticmethod
    def after_request(response):

        # 获取响应数据
        try:
            response_data = json.loads(response.data)
        except Exception:
            response_data = response.data

        log_info = {
            "host": request.host_url,
            "path": request.path,
            "method": request.method,
            "response": {
                "header": dict(response.headers),
                # 日志响应结果保留 5000个字符
                "params": str(response_data)[:500] or "UnKnown Response Data",
            }
        }
        logger.info(log_info)

        return response
