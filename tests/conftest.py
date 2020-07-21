# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
create time '2019/8/29 21:01'

Module usage:

"""
# pylint: disable=wrong-import-position,redefined-outer-name

import pytest
from redis import Redis

from app.utils import RedisAction
from app.utils.timer import current_time

# pytest 默认不会改写对非 test 函数的 assert 语句
# 激活 pytest 对 assert 的支持, 会展示更详细的信息
pytest.register_assert_rewrite('tests.base')


def pytest_report_header():
    """给测试报告的头部添加 字符串信息"""
    return [f'\033[35mIt is {current_time()} now!!!\033[0m',
            '\033[35mAuthor is rgc, if this program report error, '
            'please contact me immediately!!!\033[0m']


@pytest.fixture
def mock_redis_status(monkeypatch):
    def mock_check_redis_status(*args, **kwargs):
        return True, ''

    def mock_get_hash_ring_map(*args, **kwargs):
        return {}

    def mock_redis_delete(*args, **kwargs):
        return True

    def mock_redis_hmset(*args, **kwargs):
        return True

    def mock_redis_hgetall(*args, **kwargs):
        return {}

    monkeypatch.setattr(RedisAction, 'check_redis_status', mock_check_redis_status)
    monkeypatch.setattr(RedisAction, 'get_hash_ring_map', mock_get_hash_ring_map)

    monkeypatch.setattr(Redis, 'delete', mock_redis_delete)
    monkeypatch.setattr(Redis, 'hmset', mock_redis_hmset)
    monkeypatch.setattr(Redis, 'hgetall', mock_redis_hgetall)
