# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from flask import current_app

from app.controllers.base import BaseController
from app.core import logger
from app.libs.pre_request import Rule, pre
from app.models.distributed_redis_server_db.server_info import ServerInfoModel
from app.utils import HASH_RING_MAP, ConsistencyHash, RedisAction, ApiException, json_success, json_fail, CodeDict
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

        self.add(params)
        # 添加数据到db
        if not ServerInfoModel.create(params):
            return json_fail(CodeDict.db_error)
        return json_success()

    @classmethod
    def add(cls, params):
        """
        给 主服务器 添加缓存节点
        :param params:
        :return:
        """
        logger.info('检查是否添加 缓存节点')
        master_server_id = params.get('master_server_id')
        if not master_server_id:
            return

        # 开始添加
        logger.info('获取 主服务器相关信息')
        server_info_dict = ServerInfoModel.get_info(master_server_id)

        host = params['host']
        port = params['port']
        replicas = current_app.config.get('VNODE_REPLICAS') or 5
        new_node = RedisAction.url_format(**params)

        logger.info("判断节点 host:port 是否重复")
        master_redis_obj = RedisAction.get_redis_obj(**server_info_dict)
        hash_ring_map = RedisAction.get_hash_ring_map(master_redis_obj)
        real_node_list = list(set(hash_ring_map.values()))
        if real_node_list and f'{host}:{port}' in str(real_node_list):
            raise ApiException(500, '节点已存在')

        logger.info('检查节点能否使用')
        node_redis_obj = RedisAction.get_redis_obj(**params)
        check_result, _str = RedisAction.check_redis_status(node_redis_obj)
        if not check_result:
            raise ApiException(500, f'节点无法连接:{_str}')

        logger.info('添加节点到hash')
        real_node_list.append(new_node)
        logger.info(f'real_node_list:{real_node_list}')
        con_hash_obj = ConsistencyHash(real_node_list, replicas)
        hash_ring_map = con_hash_obj.node_info
        logger.info(f'一致性hash计算结束,hash_ring_map:{hash_ring_map}')

        logger.info('覆盖添加 hash_ring_map')
        master_redis_obj.delete(HASH_RING_MAP)
        master_redis_obj.hmset(HASH_RING_MAP, hash_ring_map)
