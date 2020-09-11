# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.libs.pre_request import Rule, pre
from app.models.distributed_redis_server_db.server_info import ServerInfoModel
from app.utils import json_success, json_fail, CodeDict
from .base import api

request_upsert_rules = {
    "memory_threshold": Rule(direct_type=float, allow_empty=True, gt=0, lt=100),
    "note": Rule(direct_type=str, allow_empty=False),
    "id": Rule(direct_type=int, allow_empty=False, gte=1),
}


@api.resource("/update")
class ServerInfoUpdateController(BaseController):
    """节点基础信息 修改"""

    @pre.catch(post=request_upsert_rules)
    def post(self, params):
        """ 节点添加 修改

        POST: /server_info/update
        """
        result = ServerInfoModel.update([ServerInfoModel.id == params.pop('id'), ServerInfoModel.state == 1], params)
        if not result:
            return json_fail(CodeDict.db_error)
        return json_success()
