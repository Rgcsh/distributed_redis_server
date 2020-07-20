# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
create time '2019/8/28 16:18'

Module usage:
测试用例
"""
import os

from app import create_app
from app.core import redis
from app.utils import HASH_RING_MAP

os.environ['FLASK_CONFIG'] = '/Users/rgc/project/distributed_redis_server/config/config_local.yml'

# 测试全局共用一个app
app = create_app()
app.config["TESTING"] = True


class TestBase(object):
    """
    测试用例基类
    此基类主要功能包括
        建立数据库连接
    """
    app = app
    client = app.test_client()

    @classmethod
    def setup_class(cls):
        """创建 flask 上下文环境, 必须执行, 否则无法使用 flask 相关拓展"""
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, 'app_context'):
            cls.app_context.pop()

    @classmethod
    def send_request(cls, url, params=None, code=200, method='get',
                     headers=None, is_json=True, test_id=None):
        """
        发送具体的数据请求到服务器
        :param url: 请求地址
        :param params: 请求参数
        :param code: 响应码
        :param test_id: 测试的唯一ID
        :param method: post请求
        :param headers:
        :param is_json:
        """

        if is_json:
            rsp = cls.client.open(path=url, method=method, json=params, headers=headers)
        else:
            rsp = cls.client.open(path=url, method=method, data=params, headers=headers)

        assert rsp.status_code == 200, f'test_id: {test_id}\n{rsp}'

        result = rsp.get_json(True)

        assert result["respCode"] == code, f'test_id: {test_id}\n{result}'

    @staticmethod
    def del_map():
        """
        删除 HASH_RING_MAP数据
        :return:
        """
        redis.delete(HASH_RING_MAP)
