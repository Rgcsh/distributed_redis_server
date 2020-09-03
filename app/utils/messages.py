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

    not_unique = 1001
    field_val_err = 1002
    data_repeat = 1003
    db_error = 1004
    no_data = 1005
    redis_err = 1006

    passwd_error_freq = 1018

    # message
    no_message = 1022


error_message = {
    # 系统错误
    200: "请求成功",
    404: "找不到相关资源",
    405: "方式不被允许",
    500: "请求处理失败",

    1001: "数据不唯一错误",
    1002: "参数值错误",
    1003: "数据重复",
    1004: "数据库错误",
    1005: "数据不存在",
    1006: "redis错误",

    1018: "密码错误过多，请24小时后重试",

    # message
    1022: "error_message中没有这个code",

    # redis
    10402: "redis内存容量不足",
    10403: "redis出错",

}
