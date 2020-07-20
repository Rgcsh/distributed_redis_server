# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""
from flask import current_app

from app.controllers.base import BaseController
from app.core import logger, redis
from app.libs.pre_request import Rule, pre
from app.utils import json_success, json_fail, HASH_RING_MAP, ConsistencyHash, RedisAction
from .base import api

request_upsert_rules = {
    "host": Rule(direct_type=str, allow_empty=False),
    "port": Rule(direct_type=int, allow_empty=False),
    "db": Rule(direct_type=int, allow_empty=False, gte=0, lte=15),
    "password": Rule(direct_type=str, allow_empty=True),
}


@api.resource("/add")
class NodeAddController(BaseController):
    """节点添加 类"""

    @pre.catch(post=request_upsert_rules)
    def post(self, params):
        """ 节点添加 接口

        POST: /node/add
        """
        host = params['host']
        port = params['port']
        replicas = current_app.config.get('VNODE_REPLICAS') or 5
        new_node = RedisAction.url_format(**params)

        logger.info("判断节点 host:port 是否重复")
        hash_ring_map = RedisAction.get_hash_ring_map()
        real_node_list = list(set(hash_ring_map.values()))
        if real_node_list and f'{host}:{port}' in str(real_node_list):
            return json_fail(message='节点已存在')

        logger.info('检查节点能否使用')
        node_redis = RedisAction.get_redis_obj(**params)
        check_result, _str = RedisAction.check_redis_status(node_redis)
        if not check_result:
            return json_fail(message=f'节点无法连接:{_str}')

        logger.info('添加节点到hash')
        real_node_list.append(new_node)
        logger.info(f'real_node_list:{real_node_list}')
        con_hash_obj = ConsistencyHash(real_node_list, replicas)
        hash_ring_map = con_hash_obj.node_info
        logger.info(f'一致性hash计算结束,hash_ring_map:{hash_ring_map}')

        logger.info('覆盖添加 hash_ring_map')
        redis.delete(HASH_RING_MAP)
        redis.hmset(HASH_RING_MAP, hash_ring_map)
        return json_success()
