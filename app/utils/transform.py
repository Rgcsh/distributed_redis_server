# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
import uuid
from copy import deepcopy
from decimal import Decimal

from .exceptions import PPInvalidMapException


def float_four(input_float, size=4):
    """ 保留四位小数

    Usage:
        >>> float_four(3.231234)
        >>> 3.2312
        >>> float_four(3.2)
        >>> 3.2
    """

    if isinstance(input_float, Decimal):
        return round(float(input_float), size)

    if isinstance(input_float, (int, float)):
        return round(input_float, size)
    return input_float


def get_value_with_field(model, field, null=None):
    """
    Get value from a model or dict or list with field
    Field must be a string or number value

    usage:

        >>> model_value_with_field({"key1": "value1", "key2": "value2"}, "key1", "default")
        "value1"
        >>> model_value_with_field({"key1": "value1", "key2": "value2"}, "key3", "default")
        "default"
        >>> model_value_with_field(["1", "2", "3"], 2, "default")
        "3"
        >>> model_value_with_field(["1", "2", "3"], 4, "default")
        "default"

    :param model: origin model or dict or list
    :param field: which value want to get
    :param null: default value if field not in model
    """
    # check input value
    if not model:
        return null

    # get value from dict
    if isinstance(model, dict):
        return model.get(field, null)

    # get value from list
    if isinstance(model, list):
        # if model is a list, field must be a number
        try:
            index = int(field)

            # check index is in the list
            if len(model) <= index:
                return null

            return list(model)[index]

        except TypeError:
            return null

    # get value from an object
    if hasattr(model, field):
        return getattr(model, field)

    return null


def decimal_2_float(ori_value, null=None):
    """ 将原始数据转换成float类型

    :param ori_value: 原始数据
    :param null: 当原始数据为None值时的默认填充
    """
    if ori_value is None:
        return null

    if isinstance(ori_value, Decimal):
        return float(ori_value)

    return ori_value


def array_column_with_key(array, column=None, append=True, key_func=None):
    """ Get item value as key, just like group by func

    Usage:
        >>> array_column_with_key([('a', 2, 3), ('b', 4, 5)], column=0)
        {'a': [('a', 2, 3)], 'b': [('b', 4, 5)]}

    :param array: origin array
    :param column: which column as key
    :param append: old value will be converd if not append
    :param key_func: func to generate new key
    :return:
    """
    # invalid input
    if not array or column is None:
        return dict()

    result_dict = dict()
    for obj in array:
        # get key value
        value = get_value_with_field(obj, column, null=None)

        # use key func to generate new key
        if key_func:
            value = key_func(value)

        # invalid value
        if value is None:
            continue

        if append:
            # exist value in result dict
            exit_value = result_dict.get(value, list())
            # store value in exit value
            exit_value.append(obj)
            result_dict[value] = exit_value
        # old value will be cover
        else:
            result_dict[value] = obj

    return result_dict


def array_index(array, index=0, null=None, ignore_empty=True):
    """ 将 字典数组 或者 二维数组 转换成一维数组
    Get sub array index value

    usage:
        >>> array_index([[1, 2], [3, 4]], 0)
        [1, 3]
        >>> array_index([[1, 2], [3, 4]], 1)
        [2, 4]

    :param array: origin array
    :param index: sub array index
    :param null: default value if empty
    :param ignore_empty: ignore value if value is empty
    """
    if not array:
        return list()

    # get sub array value with index
    result = list()
    for item in array:
        # get value
        value = get_value_with_field(item, index, null)
        # ignore value
        if not value and ignore_empty:
            continue
        # append result
        result.append(value)

    return result


def safe_float(ori_value, default=None):
    """ 完全安全的将原始数据转换成float类型

    :param ori_value: 原始数据
    :param default: 转换失败后的默认值
    :return: 格式化转换之后的数据
    """
    if ori_value is None:
        return default

    try:
        return float(ori_value)
    except TypeError:
        return default


def delete_property_in_dict(ori_dict, property_list):
    """ 删除字典中的多余元素

    Usage:
        >>> delete_property_in_dict({"key1": "value1", "key2": "value2"}, ["key1"])
        >>> {"key2": "value2"}

    :param ori_dict: 原始的字典
    :param property_list: 需要删除的key
    """
    # 属性列表为空，表示不需要删除
    if not property_list:
        return

    # 依次删除
    for prop in property_list:
        if prop in ori_dict:
            del ori_dict[prop]


def list_value_judge(first_list, last_list):
    """ 校验这个月 相对于上个月的 上升概率

    当前月减去上个月 的value 返回结果中 >0:上升 =0:持平 <0:下降

    Usage:
        >>> list_value_judge([{'sec_id': '1', 'value':4.00000000)},{'sec_id': '1', 'value':4.000000)}],
        >>>                   [{'sec_id': '1', 'value':0.00000000)},{'sec_id': '1', 'value':2.0000000)}])
        >>> [{'sec_id': '1', 'value':4.0000000000000000)},
        >>>  {'sec_id': '2', 'value':2.0000000000000000)}]

    :param first_list: 当前月
    :param last_list: 上个月
    :return:
    """

    result_list = []

    for item, _ in enumerate(first_list):
        if first_list[item]['sec_id'] == last_list[item]['sec_id']:
            _value = float_four(first_list[item]['value']) - float(last_list[item]['value'])
            if _value > 0:
                value = 1
            elif _value == 0:
                value = 2
            else:
                value = 3
            result_list.append({'sec_id': first_list[item]['sec_id'], 'value': value})
    return result_list


def dict_2d_to_list(input_dict):
    """ 获取 二维 dict中的 value 到 list 中

    Usage:
        >>> dict_2d_to_list({'a':{'c':1,'d':2},'b':{'c':3,'d':4}})
        >>> [1,2,3,4]

    :param input_dict:
    :return:
    """
    result_list = []
    for _, v in input_dict.items():
        for _, v_son in v.items():
            result_list.append(v_son)
    return result_list


def get_dict_2d_result(macro_strategy_sec_id_list_map, macro_strategy_dict):
    """ 整合数据到规定的结构

    Usage:
        >>> macro_strategy_sec_id_list_map = [{'record_type': 'win_rates', 'a_share': 'att_00000115'},
        >>>    {'record_type': 'assessment', 'a_share': 'att_00000116'},
        >>>    {'record_type': 'deploy', 'a_share': 'att_00000117'}

    :param macro_strategy_sec_id_list_map:
    :param macro_strategy_dict:
    :return:
    """
    copy_map = deepcopy(macro_strategy_sec_id_list_map)

    _result_list = []
    for _dict in copy_map:
        __dict = {}
        for k, v in _dict.items():
            if k != 'record_type':
                __dict[k] = macro_strategy_dict[v]
            else:
                __dict[k] = v
        _result_list.append(__dict)
    return _result_list


def get_dict_3d_result(map_dict, map_list):
    """ 根据 map_list中的 sec_id 和 map_dict 中的 值 比较，相同 就把 map_dict的值换为 map_list中的value值

    Usage:
        >>> get_dict_3d_result({'aa': {'a': 1, 'b': 2}, 'bb': {'c': 3, 'd': 4}},
        >>>                     [{'sec_id': 1, 'value': 'success','trade_date':'2018-01-11'},
        >>>                      {'sec_id': 2, 'value': 'suc','trade_date':'2018-01-11'},
        >>>                      {'sec_id': 3, 'value': 'suc3','trade_date':'2018-01-11'},
        >>>                      {'sec_id': 4, 'value': 'suc4','trade_date':'2018-01-11'},])

        >>> output:
        >>> {'2018-01-11':{'aa': {'a': 'success', 'b': 'suc'}, 'bb': {'c': 'suc3', 'd': 'suc4'}}}

    :param map_dict: 必须为二维dict
    :param map_list: 必须为list中包裹 dict
    :return: 返回 和map_dict 结构完全相同的dict(只有value值不同)
    """

    return_dict = dict()

    result_dict = deepcopy(map_dict)
    # 第一层
    for k, v in map_dict.items():
        # 第二层
        for k_son, v_son in v.items():

            for _ in map_list:
                trade_date = str(_['trade_date'].date())
                if trade_date in return_dict:
                    if v_son == _['sec_id']:
                        return_dict[trade_date][k][k_son] = _['value']
                else:
                    return_dict[trade_date] = result_dict
                    if v_son == _['sec_id']:
                        return_dict[trade_date][k][k_son] = _['value']
    return return_dict


def dict_filter_to_list(input_dict, filter_key):
    """ 获取 二维 dict中的部分 value 到 list 中

    Usage:
        >>> dict_filter_to_list({'a':{'c':1,'d':2},'b':{'c':3,'d':4}},'c')
        >>> [1,3]

    :param input_dict:
    :param filter_key:保留数据的key
    """
    result_list = []
    for _, v in input_dict.items():
        for k_son, v_son in v.items():
            if k_son == filter_key:
                result_list.append(v_son)
    return result_list


def dict2d_to_1d(input_dict, filter_key):
    """ 二维dict根据filter_key变为一维dict

    Usage:
        >>> dict2d_to_1d({'a':{'c':1,'d':2},'b':{'c':3,'d':4}},'c')
        >>> {'a':1,'b':1}

    :param input_dict:
    :param filter_key: 需要保留的二维key，根据此key变为1位dict
    :return:
    """
    result_dict = deepcopy(input_dict)
    for k, v in input_dict.items():
        for k_son, v_son in v.items():
            if k_son == filter_key:
                result_dict[k] = v_son
    return result_dict


def dict1d_to_include_list(input_dict, map_list):
    """ 二维dict根据filter_key变为一维dict

    Usage:
        >>> dict2d_to_1d({'a':{'c':1,'d':2},'b':{'c':3,'d':4}},'c')
        >>> {'a':1,'b':1}

     :param input_dict:
    :param map_list: 需要保留的二维key，根据此key变为1位dict
    :return:
    """
    result_dict = deepcopy(input_dict)
    for item in map_list:
        for k, v in input_dict.items():
            if item['sec_id'] == v:
                if isinstance(result_dict[k], str):
                    result_dict[k] = []
                copy_item = deepcopy(item)
                del copy_item['sec_id']
                result_dict[k].append(copy_item)
    return result_dict


def allow_value_judge(_type, value_list, enum_list):
    """ 值范围校验


    Usage:
        >>> allow_value_judge(int, [1,2,3], [1,2])
        >>> False

        >>> allow_value_judge(int, [1,2,1,2], [1,2])
        >>> True

    :param _type: 输入的值
    :param value_list: 输入类型
    :param enum_list: 校验范围
    :return: Bool
    """

    try:
        for value in value_list:
            val = _type(value)
            if val not in enum_list:
                return False
        return True
    except Exception as e:
        print(e)
        return False


def get_uuid():
    """
    生成全球唯一uuid
    :return:
    """
    return ''.join(str(uuid.uuid1()).split('-'))


def format_dict_keys(ori_dict, key_map, generate=False):
    """ 格式化字典的key, 将key进行批量替换

    :param ori_dict: 原始字典
    :param key_map: 映射的字典
    :param generate: 是否生成新的字典
    """
    if key_map is None or not isinstance(key_map, dict):
        raise PPInvalidMapException("key_map must be the instance of dict")

    # 不是生成新的字典，则以旧的字典为主，原地改变
    if generate:
        format_dict = dict()
        # 批量遍历映射的字典
        for ori_key, new_key in key_map.items():
            # 去除旧字典中的值进行替换
            format_dict[new_key] = get_value_with_field(ori_dict, ori_key, None)

        return format_dict
    # 遍历原始字典
    for ori_key in ori_dict.keys():
        # choose valid key
        key = key_map.get(ori_key, ori_key)

        # key is not exchange
        if ori_key == key:
            continue

        # replace
        ori_dict[key] = ori_dict.pop(ori_key)

    return ori_dict


def try_int(val):
    """
    尝试 转为int类型
    :param val:
    :return:
    """
    try:
        return int(val)
    except Exception:
        return val


def str2byte(_str):
    """
    str to bytes
    :param _str:
    :return:
    """
    return bytes(_str, encoding='utf8')


def byte2str(_bytes):
    """
    bytes to str
    :param _bytes:
    :return:
    """
    return str(_bytes, encoding="utf-8")
