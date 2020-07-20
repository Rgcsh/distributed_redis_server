# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""
import yagmail as yagmail

from app.controllers.node.remove import NodeRemoveController
from app.core import logger, scheduler
from app.utils import get_core_config, RedisAction


@scheduler.task('interval', id='corn_get_data', seconds=10)
def corn_check_node():
    """
    定时任务执行时间：每隔10s执行一次

    定时任务 检查每个redis node 是否可用
    几次不行之后 则 从集群中移除节点,并发送邮件给管理员
    """
    logger.info('corn_check_node job start executed!!!!')
    hash_ring_map = RedisAction.get_hash_ring_map()
    real_node_list = list(set(hash_ring_map.values()))
    error_list = []

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


def send_email(error_list):
    """
    发送邮件
    :param error_list:错误的信息
    :return:
    """
    logger.info(f'开始发送邮件:{error_list}')
    config = get_core_config()
    smtp_account = config.get("SMTP_ACCOUNT")
    smtp_password = config.get("SMTP_PASSWORD")
    smtp_host = config.get("SMTP_HOST")
    smtp_port = config.get("SMTP_PORT")
    send_email = config.get("SEND_EMAIL")
    contents = ["尊敬的管理员:", str(error_list)]
    yag = yagmail.SMTP(smtp_account, smtp_password, host=smtp_host, port=smtp_port)
    yag.send(send_email, "您在接收邮件", contents)
