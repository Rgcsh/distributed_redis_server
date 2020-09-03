# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.core import logger, scheduler
from app.models.distributed_redis_server_db.server_info import ServerInfoModel
from app.utils import RedisAction, send_email


@scheduler.task('interval', id='corn_check_memory', hours=1)
def corn_check_memory():
    """
    定时任务执行时间：每隔1h执行一次

    定时检查每个 redis node 内存是否 快要耗尽
    发现达到预警值后,发送邮件给管理员
    方法:redis配置的maxmemory值 和 已经使用的内存容量 进行比较
    目前 预警值为200M
    """
    logger.info('corn_check_node job start executed!!!!')
    # 读取上下文
    with scheduler.app.app_context():
        server_info_list = ServerInfoModel.get_connect_master_server_info()
        for server_info in server_info_list:
            master_redis_obj = RedisAction.get_redis_obj(**server_info)
            hash_ring_map = RedisAction.get_hash_ring_map(master_redis_obj)
            real_node_list = list(set(hash_ring_map.values()))
            error_list = []

            if not real_node_list:
                logger.info('没有节点无需检查')
                continue

            logger.info(f'开始检查内存是否 快要耗尽:{real_node_list}')
            for node in real_node_list:
                redis_obj = RedisAction.get_redis_obj(node)
                # todo:内存预警值 可以改为 可配置化
                success, message = RedisAction.check_redis_memory(redis_obj, 200)
                if not success:
                    error_list.append(f'节点:{node} 内存快要耗尽,{message}')
            if error_list:
                send_email(error_list)
    logger.info('corn_check_memory job end executed!')
