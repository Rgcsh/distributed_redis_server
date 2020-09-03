# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
create time '2020/4/26 21:26'

Module usage:
不要有 __bind_key__，否则建表失败
"""
# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

HOST = '127.0.0.1'
USER = "root"
PASSWD = "root"
DB = "distributed_redis_server_db"
CHARTSET = "utf8"

app = Flask(__name__, instance_relative_config=True)
# 链接数据库路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=%s' % (
    USER, PASSWD, DB, CHARTSET)
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助。
app.config['SQLALCHEMY_ECHO'] = False
# 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
app.config['SQLALCHEMY_POOL_SIZE'] = 6
db = SQLAlchemy(app)

from sqlalchemy import Column, Integer, DateTime, func, VARCHAR, Float


class AccountBase(db.Model):
    """用户表"""
    __tablename__ = 't_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(120), unique=True, nullable=False, comment='邮箱')
    password = Column(VARCHAR(360), nullable=False, comment='密码')

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())


class ServerInfoBase(db.Model):
    """服务器信息表"""
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


if __name__ == '__main__':  # 创建表
    db.create_all()
