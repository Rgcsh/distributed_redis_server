# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/11/20 16:19'

Module usage:

"""
import pickle


def pickle_dumps(input_data):
    """
    把 python数据转为 bytes 类型
    :param input_data:
    :return:
    """
    return pickle.dumps(input_data)


def pickle_loads(input_data):
    """
    把 python bytes 数据类型 转为 原来的数据类型
    :param input_data:
    :return:
    """
    return pickle.loads(input_data)
