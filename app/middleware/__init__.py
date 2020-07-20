# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
from .log import LogMiddleWare

# 中间件
MIDDLEWARE = [
    LogMiddleWare,
]
