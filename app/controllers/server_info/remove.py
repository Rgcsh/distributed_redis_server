# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.core import logger
from app.libs.pre_request import Rule, pre
from app.models.distributed_redis_server_db.server_info import ServerInfoModel
from app.utils import json_fail
from app.utils import json_success, HASH_RING_MAP, RedisAction, ApiException, CodeDict
from .base import api

request_upsert_rules = {
    "id": Rule(direct_type=int, allow_empty=False),
}


@api.resource("/remove")
class ServerInfoNodeRemoveController(BaseController):
    """删除 所有类型服务器 相关信息"""

    @pre.catch(post=request_upsert_rules)
    def post(self, params):
        """ 删除 所有类型服务器 接口
        直接对 redis数据进行删除,然后同步到 mysql

        如果是 业务节点服务器 则 只删除 业务节点相关数据
        如果是  主服务器 则 删除此主服务器及相关业务节点数据

        POST: /server_info/remove
        """
        _id = params['id']
        logger.info('获取服务器相关信息')
        server_info_dict = ServerInfoModel.get_info(_id, ['cache_type', 'master_server_id'])
        cache_type = server_info_dict['cache_type']

        self._post(server_info_dict)
        logger.info('删除 mysql中数据')
        if not ServerInfoModel.del_server(_id, cache_type):
            return json_fail(CodeDict.db_error)
        return json_success()

    @classmethod
    def _post(cls, params):
        """

        :param params:
        :param _id:
        :return:
        """
        node_url = f"{params['host']}:{params['port']}/{params['db']}"
        cache_type = params['cache_type']
        logger.info("判断节点 IP 是否存在")

        if cache_type == 1:
            # 主服务器
            redis_obj = RedisAction.get_redis_obj(**params)
            redis_obj.delete(HASH_RING_MAP)
        else:
            # 节点服务器
            logger.info('根据主服务器id找到主服务器信息')
            master_server_info_dict = ServerInfoModel.get_info(params['master_server_id'])
            master_redis_obj = RedisAction.get_redis_obj(**master_server_info_dict)
            hash_ring_map = RedisAction.get_hash_ring_map(master_redis_obj)
            real_node_list = list(set(hash_ring_map.values()))
            if node_url not in str(real_node_list):
                raise ApiException(CodeDict.field_val_err, 'node不存在')

            cls.remove_node(node_url, hash_ring_map, master_redis_obj)

    @classmethod
    def remove_node(cls, node_url, hash_ring_map, master_redis_obj):
        """
        删除节点
        :param node_url:节点url
        :param hash_ring_map:
        :param master_redis_obj:
        :return:
        """

        logger.info('删除节点')
        new_hash_ring_map = {}
        for hash_key, node in hash_ring_map.items():
            if node_url not in node:
                new_hash_ring_map[hash_key] = node

        logger.info(f'覆盖添加 new_hash_ring_map:{new_hash_ring_map}')
        master_redis_obj.delete(HASH_RING_MAP)
        if new_hash_ring_map:
            master_redis_obj.hmset(HASH_RING_MAP, new_hash_ring_map)
