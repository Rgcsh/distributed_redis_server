# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""


class CodeDict:
    """错误常量"""
    success = 200
    not_found = 404
    method_not_allow = 405
    fail = 500

    # 参数
    field_val_err = 1001

    # message
    no_message = 1022


error_message = {
    # 系统错误
    200: "请求成功",
    404: "找不到相关资源",
    405: "方式不被允许",
    500: "请求处理失败",

    # 参数
    1001: "参数错误",

    # message
    1022: "error_message中没有这个code",

    # redis
    10402: "redis内存容量不足",
    10403: "redis出错",

}
