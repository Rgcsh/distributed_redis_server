# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
import json

# 3p
from flask import make_response

from .encoder import JsonEncoder
from .messages import error_message, CodeDict
# project
from .timer import current_timestamp


def json_response(code=200, body=None, message="", extend=None, headers=None):
    """
    通用json响应方法
    :param code: 响应码
    :param body: 响应主体
    :param message: 响应的错误消息
    :param extend: 基础参数扩展
    :type extend: dict
    :param headers: 扩展响应头
    :type headers:dict
    :return: JSON
    """
    result = {
        "timestamp": current_timestamp(),
        "respCode": code,
        "respMsg": message,
        "result": body if body is not None else {}
    }

    # 如果追加了其它参数，则合并
    if extend and isinstance(extend, dict):
        result = dict(result, **extend)

    # 将结果转换成json字符串
    result = json.dumps(result, cls=JsonEncoder)

    # 生成Flask响应
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'

    # 生成自定义响应头
    if headers and isinstance(headers, dict):
        for key, value in headers.items():
            resp.headers[key] = value

    return resp


def json_success(body=None, extend=None, headers=None):
    """ 响应内容正确

    :param body: 响应体
    :param extend: 扩展参数
    :param headers: 响应头参数
    """
    return json_response(body=body, message=error_message.get(200, ""),
                         extend=extend, headers=headers)


def json_fail(code=CodeDict.fail, message=None, body=None, extend=None, headers=None):
    """ 请求出错的响应

    :param code: 响应错误识别码
    :param message: 错误友好提示内容
    :param body: 响应体
    :param extend: 扩展参数
    :param headers: 响应头参数
    """
    if not message:
        message = error_message.get(code)
        if not message:
            message = error_message.get(CodeDict.no_message)

    return json_response(code, body={} if body is None else body, message=message,
                         extend=extend, headers=headers)
