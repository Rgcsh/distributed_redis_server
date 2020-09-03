# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.core import logger, redis
from app.libs.pre_request import Rule, pre
from app.utils import json_success, json_fail, HASH_RING_MAP, RedisAction
from .base import api

request_upsert_rules = {
    "host": Rule(direct_type=str, allow_empty=False),
    "port": Rule(direct_type=int, allow_empty=False),
    "db": Rule(direct_type=int, allow_empty=False, gte=0, lte=15),
}


@api.resource("/remove")
class NodeRemoveController(BaseController):
    """节点删除 类"""

    @pre.catch(post=request_upsert_rules)
    def post(self, params):
        """ 节点删除 接口
        直接对 redis数据进行删除,然后同步到redis
        POST: /node/remove
        """
        node_url = f"{params['host']}:{params['port']}/{params['db']}"

        logger.info("判断节点 IP 是否存在")
        hash_ring_map = RedisAction.get_hash_ring_map()
        real_node_list = list(set(hash_ring_map.values()))
        if node_url not in str(real_node_list):
            return json_fail(message='node不存在')

        self.remove_node(node_url, hash_ring_map)

        return json_success()

    @classmethod
    def remove_node(cls, node_url, hash_ring_map):
        """
        删除节点
        :param node_url:节点url
        :param hash_ring_map:
        :return:
        """

        logger.info('删除节点')
        new_hash_ring_map = {}
        for hash_key, node in hash_ring_map.items():
            if node_url not in node:
                new_hash_ring_map[hash_key] = node

        logger.info(f'覆盖添加 new_hash_ring_map:{new_hash_ring_map}')
        redis.delete(HASH_RING_MAP)
        if new_hash_ring_map:
            redis.hmset(HASH_RING_MAP, new_hash_ring_map)
