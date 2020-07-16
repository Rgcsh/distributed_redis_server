# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/16 11:08'

Usage:

"""
import traceback

from func_timeout import func_set_timeout
from redis import Redis

from app.core import logger, redis
from app.utils import time_out, HASH_RING_MAP, byte2str


def url_format(*args, **kwargs):
    """
    生成redis url
    :param args:参数顺序必须为 host,port,db,password
    :param kwargs:
    :return:

    Usage:
    >>> redis_url_format('127.0.0.1', 6379, 1, 'xxx')
    >>> "redis://:xxx@127.0.0.1:6379/1"

    >>> redis_url_format(**{'host': '127.0.0.1', 'port': 6379,'db':1,'password':'xxx'})
    >>> "redis://:xxx@127.0.0.1:6379/1"
    """
    password = None
    if args:
        if len(args) == 3:
            host, port, db = args
        else:
            host, port, db, password = args
    else:
        host = kwargs.get('host')
        port = kwargs.get('port')
        db = kwargs.get('db')
        password = kwargs.get('password')

    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    else:
        return f"redis://{host}:{port}/{db}"


def get_hash_ring_map():
    """
    获取manager redis中的map,并格式化
    :return:
    """
    _dict = redis.hgetall(HASH_RING_MAP)
    new_dict = {}
    for k, v in _dict.items():
        new_dict[byte2str(k)] = byte2str(v)
    return new_dict


def get_redis_obj(*args, **kwargs):
    """
    获取 操作redis的对象
    :return:
    """
    password = None
    if args:
        if len(args) == 1:
            return Redis.from_url(args[0])
        if len(args) == 3:
            host, port, db = args
        else:
            host, port, db, password = args
    else:
        host = kwargs.get('host')
        port = kwargs.get('port')
        db = kwargs.get('db')
        password = kwargs.get('password')

    # 获取redis对象
    return Redis(host, port, db, password)


@time_out
@func_set_timeout(5)
def check_redis_status(redis_obj):
    """
    检查 redis的状态是否可用
    添加 超时5s超时自动认为连接失败
    :param redis_obj:
    :return:
    """
    try:
        ping_result = redis_obj.ping()
        return ping_result, ''
    except Exception as _:
        logger.error(traceback.format_exc())
        return False, _
