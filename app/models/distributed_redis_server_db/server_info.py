# -*- coding: utf-8 -*-
# (C) Wu Dong, 2018
# All rights reserved

from .entity import ServerInfoBase


class ServerInfoModel(ServerInfoBase):
    """服务器信息表"""
    __bind_key__ = ServerInfoBase.__bind_key__
    __tablename__ = ServerInfoBase.__tablename__

    query_list = ['id', 'host', 'port', 'db', 'password', 'memory_threshold', 'cache_type', 'note', 'state',
                  'master_server_id']
    warn_field_list = ['host', 'port', 'db', 'password']

    @classmethod
    def get_info_list_by_id(cls, _id):
        """
        根据id查询数据list
        :param _id:
        :return:
        """
        ins = cls.info_all_or([cls.id == _id, cls.master_server_id == _id])
        _list = []
        for obj in ins:
            if obj.state == 1:
                _list.append(obj.to_dict(cls.query_list))
        return _list

    @classmethod
    def get_all_info(cls):
        """
        根据id查询数据list
        :return:
        """
        return cls.info_all([cls.state == 1], cls.query_list)

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

    @classmethod
    def get_info(cls, _id, field_list=None):
        """
        获取服务信息
        :param _id:
        :return:
        """
        query_list = cls.warn_field_list
        if field_list:
            query_list += field_list
        return cls.info([cls.id == _id, cls.state == 1], query_list)

    @classmethod
    def get_connect_master_server_info(cls):
        """
        获取服务信息的连接数据
        :return:
        """
        return cls.info_all([cls.cache_type == 1], cls.warn_field_list)

    @classmethod
    def del_server(cls, _id, cache_type):
        """
        状态删除服务
        :param _id:
        :param cache_type:
        :return:
        """
        query_list = [cls.id == _id]
        if cache_type == 1:
            query_list += [cls.master_server_id == _id]
        return cls.update(query_list, {'state': 3})

    @classmethod
    def update_state(cls, info_dict):
        """
        更新状态
        :param info_dict:
        :return:
        """
        query_list = [cls.host == info_dict['host'],
                      cls.port == info_dict['port'],
                      cls.master_server_id == info_dict['master_server_id'],
                      cls.db == info_dict['db'],
                      cls.state == 1]
        return cls.update(query_list, {'state': 2})

    @classmethod
    def get_master_server_info_by_node_id(cls, _id):
        """
        根据 节点ID 找到对应主服务器相关信息
        :param _id:
        :return:
        """
        cls.info_first_and_query([cls.id == _id], cls.master_server_id)

    @classmethod
    def check_exist(cls, params):
        """
        检查是否存在
        :param params:
        :return:
        """
        _dict = {'host': params['host'], 'port': params['port'], 'db': params['db'], 'state': 1}
        return cls.exist(_dict)
