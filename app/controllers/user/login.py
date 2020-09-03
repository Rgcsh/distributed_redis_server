# -*- coding: utf-8 -*-
"""
zzmx
All rights reserved
create time '2020/2/27 13:02'
"""

from app import json_fail
from app.controllers.base import BaseController
from app.core import redis
from app.libs.pre_request import Rule, pre
from app.utils import CodeDict, json_success, get_unique_str, md5_encrypt, TOKEN_EXPIRE_TIME, \
    LOGIN_ERROR_COUNT, SUCCESS_LOGIN_TOKEN
from .base import api
from ...models.distributed_redis_server_db import AccountModel

request_rules = {
    "email": Rule(direct_type=str, trim=True, allow_empty=False, email=True),
    "password": Rule(direct_type=str, trim=True, allow_empty=True),
}


@api.resource("/login")
class LoginController(BaseController):
    """
    登录过期时间为2天，每次登录时间累加
    校验错误登录次数，防止暴力破解密码攻击,过期时间为1天
    """

    @pre.catch(post=request_rules)
    def post(self, params):
        email = params["email"]
        password = params["password"]

        # 校验错误登录次数，防止暴力破解密码攻击
        login_error_key = LOGIN_ERROR_COUNT.format(email)
        login_error_key_count = redis.get(login_error_key)
        if not login_error_key_count:
            redis.set(login_error_key, 1, 86400)
        elif int(login_error_key_count) > 10:
            return json_fail(CodeDict.passwd_error_freq)

        # 获取用户信息
        result = AccountModel.get_info_by_email(email)
        if not result:
            return json_fail(CodeDict.fail, '未注册')

        db_passwd = result.pop('password')
        if md5_encrypt(password) != db_passwd:
            return json_fail(CodeDict.fail, '密码错误')

        # 收尾工作
        redis.delete(login_error_key)

        # 生成token
        token = get_unique_str()
        key = SUCCESS_LOGIN_TOKEN.format(token)
        redis.set(key, email, TOKEN_EXPIRE_TIME)
        result['token'] = token

        return json_success(result)
