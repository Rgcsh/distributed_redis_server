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
from .constant import HASH_RING_MAP
from .timer import time_out
from .transform import byte2str


class RedisAction:
    """redis操作类"""

    @staticmethod
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

    @staticmethod
    def split_url_format(url: str):
        """
        把 redis url分析出 host,port,db, password
        :param url:
        :return:
        """
        _url = url.split('redis://')[1]
        if '@' in _url:
            _password, _url = _url.split('@')
            password = _password.split(':')[1]
            host, _url = _url.split(':')
            port, db = _url.split('/')
            return {'host': host, 'port': port, 'db': db, 'password': password}
        else:
            host, _url = _url.split(':')
            port, db = _url.split('/')
            return {'host': host, 'port': port, 'db': db, 'password': None}

    @staticmethod
    def get_hash_ring_map(redis_obj=None):
        """
        获取manager redis中的map,并格式化
        :return:
        """
        if not redis_obj:
            redis_obj = redis
        _dict = redis_obj.hgetall(HASH_RING_MAP)
        new_dict = {}
        for k, v in _dict.items():
            new_dict[byte2str(k)] = byte2str(v)
        return new_dict

    @staticmethod
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

    @staticmethod
    def redis_from_url(node_url):
        """
        通过url获取redis对象
        注意:此处获取的redis对象是直接从redis包导入的,可以进行任何操作,不会对 execute_command进行修改
        :param node_url:
        :return:
        """
        return redis.from_url(node_url)

    @staticmethod
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
            # 能否ping通
            redis_obj.ping()
            # 分配的内存是否够用
            redis_obj.setex('test:distributed_redis_server', 1, 1)
            return True, ''
        except Exception as _:
            logger.error(traceback.format_exc())
            return False, _

    @classmethod
    @time_out
    @func_set_timeout(5)
    def get_redis_memory(cls, redis_obj):
        """
        获取redis 内存信息
        :param redis_obj:
        :return:
        """
        try:
            memory_dict = redis_obj.info('Memory')
            # 已经使用内存容量
            used_memory = memory_dict.get('used_memory')
            # 设置最大内存容量
            maxmemory = memory_dict.get('maxmemory')
            if maxmemory == 0:
                memory_dict['can_use_rate'] = None
            else:
                # 可以使用最大内存容量
                can_use_rate = used_memory / maxmemory
                memory_dict['can_use_rate'] = can_use_rate
            return True, memory_dict
        except Exception as _:
            logger.error(traceback.format_exc())
            return False, {'used_memory': '', 'maxmemory': '', 'can_use_rate': ''}

    @classmethod
    def check_redis_memory(cls, redis_obj, memory_limit_rate):
        """
        检查 redis的状态是否可用
        添加 超时5s超时自动认为连接失败
        :param redis_obj:
        :param memory_limit_rate: 内存限制率
        :return:
        """
        status, memory_dict = cls.get_redis_memory(redis_obj)
        if not status:
            return False, '获取redis内存信息失败'
        can_use_rate = memory_dict.get('can_use_rate')
        if can_use_rate is None:
            return False, '没有设置内存限制:maxmemory,请尽快设置'
        if can_use_rate and can_use_rate < memory_limit_rate:  # M转为 bytes
            return False, f'maxmemory:{memory_dict.get("used_memory_human")},' \
                          f'used_memory:{memory_dict.get("maxmemory_human")},可用内存使用率:{can_use_rate}'
        return True, ''
