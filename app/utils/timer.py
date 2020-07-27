# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
import datetime
import time

from func_timeout import FunctionTimedOut


def date_2_datetime(ori_date):
    """
    日期格式数据转为日期时间
    :param ori_date:
    :return:
    """
    if isinstance(ori_date, datetime.date):
        return datetime.datetime(ori_date.year, ori_date.month, ori_date.day)
    return ori_date


def current_timestamp():
    """
    生成当前日期的时间戳
    """
    return int(time.time())


def current_time(formatter="%Y-%m-%d %H:%M:%S"):
    """
    Get current datetime with format

    Usage:
        >>> current_time("%Y-%m-%d")
        "2018-09-03"
        >>> current_time("%Y-%m-%d %H:%M:%S")
        “2018-09-03 11:35:29”

    :param formatter: format of datetime
    :return: type:str
    """
    return datetime.datetime.now().strftime(formatter)


def current_datetime():
    """ 获取当前的日期
    """
    return datetime.datetime.now()


def timestamp_2_datetime(timestamp, formatter="%Y-%m-%d %H:%M:%S"):
    """ 将时间戳转换为指定格式的日期

    :param timestamp: 原始时间戳
    :param formatter: 时间格式
    """
    return time.strftime(formatter, time.localtime(timestamp))


def datetime_2_timestamp(ori_datetime):
    """ 间隔日期转换成时间戳

    :param ori_datetime: 原始日期
    """
    return int(time.mktime(ori_datetime.timetuple()))


def datetime_2_str(ori_datetime, formatter="%Y-%m-%d %H:%M:%S", default=None):
    r"""
    Transform datetime type params to string type

    Usage:
        >>> datetime_2_str(datetime(1991, 4, 3), "%Y-%m-%d")
        1991-04-03

    :param ori_datetime: user input datetime
    :param formatter: formatter
    :param default: default value if input invalid
    :return:
    """
    # invalid input
    if not ori_datetime:
        return default

    # input value is string
    if isinstance(ori_datetime, str):
        return ori_datetime

    return ori_datetime.strftime(formatter)


def str_2_datetime(ori_str, formatter="%Y-%m-%d %H:%M:%S", default=None):
    """
    transform string type params to datetime type

    Usage:
        >>> str_2_datetime("2018-09-03", "%Y-%m-%d")
        "2018-09-03 00:00:00"

    :param ori_str: input string data
    :param formatter: transform format
    :param default: default value
    :return: formatted datetime
    :rtype datetime
    """
    try:
        # if no input value, it will return current date
        if not ori_str:
            return default

        # input type is datetime
        if isinstance(ori_str, datetime.datetime):
            return ori_str

        # input type is string
        if isinstance(ori_str, str):
            return datetime.datetime.strptime(ori_str, formatter)

    # transform with formatter failed
    except Exception:  # pylint: disable=bad-option-value,broad-except
        return default

    # invalid input
    return default


def verify_date_format(this_time, formatter="%Y-%m-%d"):
    """
    校验输入的日期格式 及 日期范围是否正确
    :param this_time:
    :param formatter: 日期格式 如：%Y-%m-%d %H:%M:%S
    :return:
    """
    try:
        time.strptime(this_time, formatter)
        return True
    except Exception:
        return False


def time_out(fn, *args, **kwargs):  # pylint:disable=unused-argument
    """
    超时的装饰器
    :param fn:
    :param args:
    :param kwargs:
    :return:
    """

    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            return result
        except FunctionTimedOut:
            return False, '请检查配置'

    return wrapper

# def func_line_time(f):
#     """
#     查询接口中每行代码执行的时间,用法为 在请求方式函数上加此装饰器
#     :param f:
#     :return:
#
#     Usage:
#     >>>@api.resource("/update/pro_asset_return")
#     >>>class UpdateProAssetReturnController():
#     >>>    @func_line_time
#     >>>    def post(self, *args, **kwargs):
#     """
#     from line_profiler import LineProfiler
#     from functools import wraps
#
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         func_return = f(*args, **kwargs)
#         lp = LineProfiler()
#         lp_wrap = lp(f)
#         lp_wrap(*args, **kwargs)
#         lp.print_stats()
#         return func_return
#
#     return decorator
