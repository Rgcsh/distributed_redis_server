# -*- coding: utf-8 -*-
"""
zzmx
All rights reserved
create time '2020/2/27 13:02'
"""
import logging

from flask import request, g

from app.core import redis
from app.models.distributed_redis_server_db.account import AccountModel
from app.utils import CodeDict, json_fail
from .base import BaseMiddleWare

logger = logging.getLogger()


class TokenMiddleWare(BaseMiddleWare):
    """记录Token的中间件"""

    @staticmethod
    def before_request():
        """
        授权中间件
        存储当前登录用户信息
        """
        token = request.values.get('token') or request.headers.get('token')
        if token:
            email = redis.get('LOGIN_TOKEN:{}'.format(token))
            # redis中不存在 email
            if not email:
                return json_fail(CodeDict.fail, 'token过期')
            user_obj = AccountModel.get_obj_by_field([AccountModel.email == email])
            # 数据库中不存在 email
            if not user_obj:
                return json_fail(CodeDict.fail, '用户不存在')

            # 获取用户基本信息
            user_info = user_obj.to_dict(AccountModel.query_list)
            user_info['token'] = token

            g.account = user_info
        else:
            # 其他蓝图里的不用校验的接口
            unjudge_url = [
                '/user/forget/password',
                '/user/login',
                '/user/register',
                '/',
            ]
            unjudge_blueprint = ['/upload']

            # 不需要登录token的路由
            url_rule = str(request.path)
            for item in unjudge_blueprint:
                if url_rule.startswith(item):
                    return

            if url_rule not in unjudge_url:
                return json_fail(CodeDict.fail, '需要token')
