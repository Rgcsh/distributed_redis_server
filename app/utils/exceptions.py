# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""


class PPException(Exception):
    """ 项目异常基类
    """

    def __init__(self, code=500, message=None):
        super().__init__()
        self.code = code
        self.message = message


class ApiException(PPException):
    """distributed_redis_server项目的API处理时的基础异常"""

    def __init__(self, code=500, message=None):  # pylint:disable=useless-super-delegation
        super().__init__(code, message)


class PPInvalidMapException(PPException):
    """ 无效的Map类型
    """


def raise_exception(response):
    """
    解析 json_fail() 并 抛出异常
    :param response:
    :return:
    """
    raise ApiException(response.json['respCode'], response.json['respMsg'])
