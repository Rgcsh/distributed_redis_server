# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
import calendar
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


def get_month_range(this_time=None, is_last_month=False, is_include_time=True):
    """
    根据年月日获取月份的起止日期，必须先执行 verify_date_format（）函数，否则没法保证 不报错
    默认返回当前日期时间所在月份范围

    Usage:
        >>> get_month_range()
        >>>

    :param this_time: str 字符串 如果不传值，表示获取当月日期范围
    :param is_last_month: 是否根据输入月份获取上个月月份范围
    :param is_include_time: 返回值是否包括 时分秒的范围
    :return: str
    """

    if this_time:
        time_format = time.strptime(this_time, "%Y-%m-%d")
    else:
        time_format = time.localtime()

    year = time_format.tm_year
    month = time_format.tm_mon

    if is_last_month:
        if month == 1:
            month = 12
            year -= 1
        else:
            month = month - 1

    day_begin = "%d-%02d-01" % (year, month)

    wday, month_range = calendar.monthrange(year, month)  # pylint:disable=unused-variable
    day_end = "%d-%02d-%02d" % (year, month, month_range)

    if is_include_time:
        day_begin = "{} 00:00:00".format(day_begin)
        day_end = "{} 23:59:59".format(day_end)

    return day_begin, day_end


def get_pre_month(str_date):
    """
    获取上个月一号

    Usage:
        >>> get_pre_month('2018-11-23')
        >>> '2018-10-01'

        >>> get_pre_month('2019-01-23')
        >>> '2018-12-01'

    :param str_date:
    :return:
    """

    try:
        time_format = time.strptime(str_date, "%Y-%m-%d")
        year = time_format.tm_year
        month = time_format.tm_mon
        if month == 1:
            month = 12
            year -= 1
        else:
            month = month - 1
        return "%d-%02d-01" % (year, month)
    except Exception as e:
        print(e)
        return False


def get_this_month_first_day():
    """
    获取本月一号
    :return: '2019-09-01'
    """

    str_date = datetime_2_str(current_time("%Y-%m-%d"), "%Y-%m-%d")
    return str_date[: 0 - 2] + "01"


def get_next_month(str_date):
    """
    获取下个月一号

    Usage:
        >>> get_next_month('2018-11-23')
        >>> '2018-12-01'

        >>> get_next_month('2018-12-23')
        >>> '2019-01-01'

    :param str_date:
    :return:
    """

    try:
        time_format = time.strptime(str_date, "%Y-%m-%d")
        year = time_format.tm_year
        month = time_format.tm_mon
        if month == 12:
            month = 1
            year += 1
        else:
            month = month + 1
        return "%d-%02d-01" % (year, month)
    except Exception:
        return False


def judge_same_month(input_month_list):
    """
    判断 数据 是否 在同一个月
    :param input_month_list:list
    :return: str or bool
    """
    month_list = []
    for item in input_month_list:
        month_list.append(item["trade_date"].strftime("%Y-%m"))
    month_set = set(month_list)
    if len(month_set) != 1:
        return False
    month_str = month_set.pop()
    # '2018-11-01'
    return month_str + "-01"


def verify_date_grater_than_now(judge_date):
    """
    验证 输入的时间大于当前时间
    :param judge_date:
    :return:
    """
    if isinstance(judge_date, str):
        judge_date = str_2_datetime(judge_date, "%Y-%m-%d")
    if judge_date > str_2_datetime(current_time("%Y-%m-%d"), "%Y-%m-%d"):
        return False
    return True


def this_month_first_day():
    """
    获取本月1号日期，返回date格式数据
    :return:
    """
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    return str_2_datetime(f"{year}-{month}-01", "%Y-%m-%d").date()


def judge_month(input_data: str):
    """
    判断 输入的时间是否为 大于当前时间;如果输入时间大于当前时间 返回True

    :param input_data:
    :return:

    Usage:
    >>> judge_month('2019-09-01')
    >>> False # current_time_str='2019-08-16'
    >>> judge_month('2019-08-01')
    >>> True # current_time_str='2019-08-16'
    """
    current_time_str = current_time("%Y-%m-%d")
    if input_data > current_time_str:
        return True
    return False


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


def time_out(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            return result
        except FunctionTimedOut:
            return False, '请检查配置'

    return wrapper
