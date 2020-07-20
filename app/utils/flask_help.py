# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/9/18'
"""
import urllib.parse

from flask import request


def cache_key():
    """
    获取请求路径及参数，并转化为字符串返回；主要用在 函数根据不同参数设置缓存时使用
    :return:
    """
    args = request.args
    li = [(k, v) for k in sorted(args) for v in sorted(args.getlist(k))]
    key = request.path + "?" + urllib.parse.urlencode(li)
    return key
