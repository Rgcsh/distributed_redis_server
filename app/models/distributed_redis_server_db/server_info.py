# -*- coding: utf-8 -*-
# (C) Wu Dong, 2018
# All rights reserved

from .entity import ServerInfoBase


class ServerInfoModel(ServerInfoBase):
    """服务器信息表"""
    __bind_key__ = ServerInfoBase.__bind_key__
    __tablename__ = ServerInfoBase.__tablename__

    query_list = ['id', 'host', 'port', 'db', 'password', 'ip_address', 'memory_threshold', 'cache_type', 'note', 'state']
    warn_field_list = ['host', 'port', 'db', 'password']

    @classmethod
    def get_info_list_by_id(cls, _id):
        """
        根据id查询数据list
        :param _id:
        :return:
        """
        return cls.info([cls.id == _id, cls.master_server_id == _id], cls.query_list)

    @classmethod
    def get_master_server_info(cls):
        """
        获取 主服务器 相关信息
        :return:
        """
        result = cls.info_all_and_query([cls.cache_type == 1, cls.state != 3], cls.id, cls.note)
        _list = []
        for item in result:
            _list.append({'id': item[0], 'note': item[1]})
        return _list
