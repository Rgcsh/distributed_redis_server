# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
"""
from sqlalchemy import Column, Integer, DateTime, func, VARCHAR, Float

from app.core import Base
from app.models.base import BaseModel

BIND_KEY = 'distributed_redis_server_db'


class AccountBase(Base, BaseModel):
    """用户表"""
    __bind_key__ = BIND_KEY
    __tablename__ = 't_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(120), unique=True, nullable=False, comment='邮箱')
    password = Column(VARCHAR(360), nullable=False, comment='密码')

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())


class ServerInfoBase(Base, BaseModel):
    """服务器信息表"""
    __bind_key__ = BIND_KEY
    __tablename__ = 't_server_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(VARCHAR(120), unique=True, nullable=False, comment='IP地址')
    port = Column(Integer, nullable=False, comment='端口')
    db = Column(Integer, nullable=False, comment='db号')
    password = Column(VARCHAR(360), nullable=True, comment='密码')
    memory_threshold = Column(Float, nullable=True, comment='内存阈值(百分比)')
    cache_type = Column(Integer, nullable=False, comment='机器功能类型(1:主服务器[负责分发等任务] 2:实际缓存机器)')
    master_server_id = Column(Integer, nullable=True, comment="主服务器ID(cache_type=2时 必填)")
    note = Column(VARCHAR(120), nullable=False, comment='服务器备注或别名')

    state = Column(Integer, nullable=False, server_default='1', comment='服务器状态(1:正常 2:失效(被集群移除) 3:已删除[不再使用])')
    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())
