# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
import hashlib
import random
import time
import uuid


def get_seed(string='', length=32):
    """
    获取特定长度的随机字符串
    热点：任意两次的字符串不相同
    """
    string += str(time.time())

    uuid_str = str(uuid.uuid1()).replace("-", "")
    string += uuid_str

    sha512 = hashlib.sha512()
    sha512.update(bytes(string, encoding="utf-8"))
    string = sha512.hexdigest()

    return string[:length]


def get_random_int() -> int:
    """
    获取 2**32 -1= 4294967295 范围内的随机整数
    :return:
    """
    return random.randint(0, 2 ** 32 - 1)


def md5_encrypt(passwd):
    """md5两次加密"""
    m = hashlib.md5()
    m.update(passwd.encode("utf8"))
    sign = m.hexdigest()
    m1 = hashlib.md5()
    m1.update(sign.encode("utf8"))
    return m.hexdigest()
