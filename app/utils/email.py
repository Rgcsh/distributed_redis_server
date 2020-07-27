# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
create time '2020/7/27 15:24'

Usage:

"""
import yagmail

from app.core import logger
from .path import get_core_config


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
    send_user = config.get("SEND_EMAIL")
    contents = ["尊敬的管理员:", str(error_list)]
    yag = yagmail.SMTP(smtp_account, smtp_password, host=smtp_host, port=smtp_port)
    yag.send(send_user, "您在接收邮件", contents)
