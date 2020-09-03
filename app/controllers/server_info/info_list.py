# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.libs.pre_request import pre, Rule
from app.models.distributed_redis_server_db.server_info import ServerInfoModel
from app.utils import json_success, RedisAction
from .base import api

request_rules = {
    "id": Rule(direct_type=int, allow_empty=False),
}


@api.resource("/info_list")
class ServerInfoListController(BaseController):
    """获取 某一个主服务 及相关业务节点 的相关信息"""

    @pre.catch(get=request_rules)
    def get(self, params):
        """
        POST: /server_info/info_list
        """
        _list = ServerInfoModel.get_info_list_by_id(params.get('id'))
        for node in _list:
            redis_obj = RedisAction.get_redis_obj(node)
            _, memory_dict = RedisAction.get_redis_memory(redis_obj)
            node.update(memory_dict)
            for field in ServerInfoModel.warn_field_list:
                node.pop(field)

        return json_success(_list)
