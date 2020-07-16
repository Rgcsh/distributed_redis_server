# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2019/9/19 10:18'
"""
from flask import Blueprint

from app.controllers.base import BaseApi

tasks = Blueprint("tasks", __name__)
api = BaseApi(tasks)
