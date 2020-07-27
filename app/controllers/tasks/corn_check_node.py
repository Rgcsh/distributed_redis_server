# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.node.remove import NodeRemoveController
from app.core import logger, scheduler
from app.utils import RedisAction, send_email


@scheduler.task('interval', id='corn_check_node', seconds=10)
def corn_check_node():
    """
    定时任务执行时间：每隔10s执行一次

    定时任务 检查每个 redis node 是否可用
    几次不行之后 则 从集群中移除节点,并发送邮件给管理员
    """
    logger.info('corn_check_node job start executed!!!!')
    hash_ring_map = RedisAction.get_hash_ring_map()
    real_node_list = list(set(hash_ring_map.values()))
    error_list = []

    if not real_node_list:
        logger.info('没有节点无需检查')
        return

    logger.info(f'开始检查:{real_node_list}')
    for node in real_node_list:
        redis_obj = RedisAction.get_redis_obj(node)
        status, message = RedisAction.check_redis_status(redis_obj)
        if not status:
            NodeRemoveController.remove_node(node, hash_ring_map)
            error_list.append(f'节点:{node} 连接失败,原因:{message}')
    if error_list:
        send_email(error_list)
    logger.info('corn_check_node job end executed!')
