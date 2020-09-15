# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""
from app.controllers.server_info.remove import ServerInfoNodeRemoveController
from app.core import logger, scheduler
from app.models.distributed_redis_server_db.server_info import ServerInfoModel
from app.utils import RedisAction, send_email


@scheduler.task('interval', id='corn_check_node', seconds=10)
def corn_check_node():
    """
    定时任务执行时间：每隔10s执行一次

    定时任务 检查每个 redis node 是否可用
    几次不行之后 则 从集群中移除节点,并发送邮件给管理员
    """
    logger.info('corn_check_node job start executed!!!!')
    # 读取上下文
    with scheduler.app.app_context():
        all_server_info_list = ServerInfoModel.get_all_info()
        logger.info(f'获取 所有服务器信息成功')
        error_list = []
        for server_info in all_server_info_list:
            if server_info.get('cache_type') == 1:
                # 主服务器检查
                master_redis_obj = RedisAction.get_redis_obj(**server_info)
                hash_ring_map = RedisAction.get_hash_ring_map(master_redis_obj)
                real_node_list = list(set(hash_ring_map.values()))

                if not real_node_list:
                    logger.info('没有节点无需检查')
                    continue

                logger.info(f'开始检查:{real_node_list}')
                for node in real_node_list:
                    redis_obj = RedisAction.get_redis_obj(node)
                    status, message = RedisAction.check_redis_status(redis_obj)
                    if not status:
                        logger.info('修改db状态为 失效')
                        node_dict = {'master_server_id': server_info.get('id')}
                        node_dict.update(RedisAction.split_url_format(node))
                        if not ServerInfoModel.update_state(node_dict):
                            raise Exception(f'修改节点状态失败,node:{node}')
                        logger.info('移除节点')
                        ServerInfoNodeRemoveController.remove_node(node, hash_ring_map, master_redis_obj)
                        error_list.append(f'节点:{node} 连接失败,原因:{message}')

        if error_list:
            send_email(error_list)

    logger.info('corn_check_node job end executed!')
