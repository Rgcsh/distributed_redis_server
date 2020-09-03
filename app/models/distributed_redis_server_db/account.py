# -*- coding: utf-8 -*-
# (C) Wu Dong, 2018
# All rights reserved

from .entity import AccountBase


class AccountModel(AccountBase):
    """用户表"""
    __bind_key__ = AccountBase.__bind_key__
    __tablename__ = AccountBase.__tablename__

    query_list = ['id', 'email', 'password']

    @classmethod
    def get_info_by_email(cls, email):
        """
        根据邮箱查询数据
        :param email:
        :return:
        """
        return cls.info([cls.email == email], cls.query_list)
