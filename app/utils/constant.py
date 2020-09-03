# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
# key:虚拟节点的hash值 到 val:真实节点的映射 dict;redis数据结构为:hash
HASH_RING_MAP = 'HASH_RING_MAP'

# reids key
# 校验发送邮件间隔
RESET_PASSWD_TIMELOOP = 'RESET_PASSWD_TIMELOOP:MOBILE:{}'
# 忘记密码时，发送邮件需要生成一个token
FORGET_RESET_PASSWD = 'RESET_PASSWD:MOBILE:{}'
# 校验错误登录次数，防止暴力破解密码攻击
LOGIN_ERROR_COUNT = 'LOGIN_ERROR_COUNT:MOBILE:{}'
# 验证码登录方式时的 验证码
LOGIN_TOKEN = 'LOGIN:{}'
# 成功登录后生成的token
SUCCESS_LOGIN_TOKEN = 'LOGIN_TOKEN:{}'
# 注册时的 验证码
REGISTER_TOKEN = 'REGISTER:{}'
# 公司用户注册时的 验证码
COMPANY_REGISTER_TOKEN = 'COMPANY_REGISTER:{}'
# 校验手机号发送次数
MOBILE_SEND_COUNT = 'MOBILE_SEND_COUNT:{}'
# token过期时间 默认2天
TOKEN_EXPIRE_TIME = 172800 * 100
