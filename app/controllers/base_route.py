# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
create time '2020/9/2 16:28'

Usage:
基础路由 "/" 下的所有视图
"""
import os

from flask import redirect, url_for, current_app, send_from_directory


def index():
    """
    url='/'
    服务根路由
    :return:
    """
    return redirect(url_for('.index', _external=True) + current_app.config['FRONT_URL'] + 'index.html')


def register_base_route(flask_app):
    """
    注册基础路由
    :param flask_app:
    :return:
    """
    flask_app.add_url_rule('/', view_func=index)

    @flask_app.route('/upload/<path:path>')
    def send_file(path):
        """
        获取图片
        """
        dirpath = os.path.join(os.path.dirname(os.path.join(flask_app.root_path)), 'upload/')
        return send_from_directory(dirpath, path)
