# -*- coding: utf-8 -*-
"""
zzmx
All rights reserved
create time '2020/2/27 13:02'
"""

from app import json_fail
from app.controllers.base import BaseController
from app.core import logger
from app.libs.pre_request import Rule, pre
from app.models.distributed_redis_server_db import AccountModel
from app.utils import json_success, CodeDict, md5_encrypt
from app.utils.flask_help import get_user_id
from .base import api

request_rules = {
    "password": Rule(direct_type=str, trim=True, allow_empty=False),
}


@api.resource("/reset/password")
class ResetPasswordController(BaseController):
    """
    重置密码
    """

    @pre.catch(post=request_rules)
    def post(self, params):
        password = params["password"]
        uid = get_user_id()
        new_password = md5_encrypt(password)

        logger.info('修改密码')
        if not AccountModel.update([AccountModel.id == uid], {'password': new_password}):
            return json_fail(CodeDict.db_error)
        return json_success()
