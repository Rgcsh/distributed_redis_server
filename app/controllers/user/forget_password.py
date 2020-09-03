# -*- coding: utf-8 -*-
"""
zzmx
All rights reserved
create time '2020/2/27 13:02'
"""
import yagmail
from flask import current_app

from app import json_fail
from app.controllers.base import BaseController
from app.libs.pre_request import Rule, pre
from app.utils import json_success, CodeDict, md5_encrypt, get_unique_str
from .base import api
from ...core import logger
from ...models.distributed_redis_server_db import AccountModel

request_rules = {
    "email": Rule(direct_type=str, trim=True, allow_empty=False, email=True),
}


@api.resource("/forget/password")
class ForgetPasswordController(BaseController):
    """
    忘记密码
    邮件 内容 为新密码
    """

    @pre.catch(post=request_rules)
    def post(self, params):
        smtp_account = current_app.config.get("SMTP_ACCOUNT")
        smtp_password = current_app.config.get("SMTP_PASSWORD")
        smtp_host = current_app.config.get("SMTP_HOST")
        smtp_port = current_app.config.get("SMTP_PORT")
        email = params["email"]

        # 判断是否存在
        if not AccountModel.exist_by_obj([AccountModel.email == email]):
            return json_fail(CodeDict.fail, '邮箱不存在')

        uuid_str = get_unique_str()[:6]
        logger.info(f'密码为:{uuid_str}')
        new_password = md5_encrypt(uuid_str)

        AccountModel.update([AccountModel.email == email], {'password': new_password}, False, False)

        contents = ["重置密码,新密码为:", uuid_str]
        yag = yagmail.SMTP(smtp_account, smtp_password, host=smtp_host, port=smtp_port)
        yag.send(email, "您在接收邮件", contents)

        if not AccountModel.commit():
            return json_fail(CodeDict.db_error)
        return json_success()
