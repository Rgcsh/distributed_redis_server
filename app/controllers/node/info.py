# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.utils import json_success, RedisAction
from .base import api


@api.resource("/info")
class NodeInfoController(BaseController):
    """节点信息 类"""

    def post(self):
        """ 获取节点 相关信息 接口
        调用 info 命令
        todo: 可能会被删除此功能
        POST: /node/info
        """
        hash_ring_map = RedisAction.get_hash_ring_map()
        real_node_list = list(set(hash_ring_map.values()))
        result_info = []
        for node_url in real_node_list:
            redis_obj = RedisAction.redis_from_url(node_url)
            info_dict = redis_obj.info()
            result_info.append({'node_url': node_url, 'node_info': info_dict})

        return json_success(result_info)
