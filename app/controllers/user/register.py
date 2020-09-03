# -*- coding: utf-8 -*-
"""
zzmx
All rights reserved
create time '2020/2/27 13:02'
"""

from app.controllers.base import BaseController
from app.libs.pre_request import Rule, pre
from app.models.distributed_redis_server_db import AccountModel
from app.utils import json_success, CodeDict, md5_encrypt, json_fail
from .base import api

request_rules = {
    "email": Rule(direct_type=str, trim=True, allow_empty=False, email=True),
    "password": Rule(direct_type=str, trim=True, allow_empty=False),
}


@api.resource("/register")
class RegisterController(BaseController):
    """
    注册接口
    """

    @pre.catch(post=request_rules)
    def post(self, params):
        email = str(params["email"])
        passwd = params["password"]

        # add to db
        result = AccountModel.create({"email": email, "password": md5_encrypt(passwd)}, unique_catch=True)
        if result == 'success':
            return json_success()
        elif result == 'not_unique':
            return json_fail(CodeDict.fail, '邮箱已注册')
        else:
            return json_fail(CodeDict.db_error)
