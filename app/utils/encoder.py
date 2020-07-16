# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
import datetime
import decimal
import json
from bson import ObjectId


class JsonEncoder(json.JSONEncoder):
    """json处理类"""
    def default(self, o):  # pylint: disable=method-hidden

        # 处理datetime
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        # 处理日期
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")

        # 处理decimal
        if isinstance(o, decimal.Decimal):
            return float(o)

        if isinstance(o, ObjectId):
            return str(o)

        # 其它默认处理
        return json.JSONEncoder.default(self, o)
