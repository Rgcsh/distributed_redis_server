# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.controllers.node.add import NodeAddController
from app.libs.pre_request import Rule, pre
from app.models.distributed_redis_server_db.server_info import ServerInfoModel
from app.utils import json_success, json_fail, CodeDict
from .base import api

request_upsert_rules = {
    "host": Rule(direct_type=str, allow_empty=False),  # 尽量用内网地址
    "port": Rule(direct_type=int, allow_empty=False),
    "db": Rule(direct_type=int, allow_empty=False, gte=0, lte=15),
    "password": Rule(direct_type=str, allow_empty=True),
    "memory_threshold": Rule(direct_type=float, allow_empty=True, gt=0, lt=100),
    "cache_type": Rule(direct_type=int, allow_empty=False, enum=[1, 2]),
    "master_server_id": Rule(direct_type=int, allow_empty=True),
    "note": Rule(direct_type=str, allow_empty=False),
}


@api.resource("/add")
class ServerInfoAddController(BaseController):
    """节点基础信息添加"""

    @pre.catch(post=request_upsert_rules)
    def post(self, params):
        """ 节点添加 接口

        POST: /server_info/add
        """

        NodeAddController.add(params)
        # 添加数据到db
        if not ServerInfoModel.create(params):
            return json_fail(CodeDict.db_error)
        return json_success()
