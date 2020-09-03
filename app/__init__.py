# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/9/16 10:21'

Module usage:

"""
import importlib
import os

from flask import Flask
from flask_cors import CORS

import app.core as core
from app import controllers
from app.controllers.base_route import register_base_route
from app.middleware import MIDDLEWARE
from app.middleware.base import BaseMiddleWare
from app.utils import json_fail, JsonEncoder
from config import Config


def configure_blueprints(flask_app):
    """
    Register BluePrints for flask
    :param flask_app: Flask的实例
    :return:
    """
    controller_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'controllers')

    for module_name in controllers.__all__:
        module_path = os.path.join(controller_dir, module_name)

        assert os.path.isdir(module_path) and not module_name.startswith('__'), \
            f'{module_name} 不是有效的文件夹, 无法导入模块'

        # 预导入所有接口文件
        for file_name in os.listdir(module_path):
            if file_name.endswith('.py') and not file_name.startswith('__'):
                module = importlib.import_module(
                    f'app.controllers.{module_name}.{file_name[:-3]}')
        # 导入模块并注册蓝图
        module = importlib.import_module(f'app.controllers.{module_name}.base')
        flask_app.register_blueprint(
            getattr(module, module_name), url_prefix=('/' + module_name))

    # 注册 / 下的view
    register_base_route(flask_app)


def configure_middleware(flask_app):
    """
    Register middleware for flask
    :param flask_app: flask app
    """
    for middle in MIDDLEWARE:
        flask_app.before_request(middle.before_request)
        flask_app.after_request(middle.after_request)


def _config_app(app):
    """ 将配置文件读取Flask对象
    """
    conf = Config(app)
    app.config.from_object(conf)
    conf.init_extensions(app)


def create_app():
    """
    Create an app with config file
    :return: Flask App
    """
    # init a flask app
    app = Flask(__name__)

    # 从yaml文件中加载配置，此加载方式有效加载
    # 初始化APP
    _config_app(app)

    # 允许跨域请求
    if app.config.get('CORS_ENABLE'):
        CORS(app)

    # 配置蓝图
    configure_blueprints(app)

    # 配置中间件
    configure_middleware(app)

    return app
