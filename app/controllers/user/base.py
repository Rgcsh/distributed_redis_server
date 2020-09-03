# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
"""
from flask import Blueprint

from app.controllers.base import BaseApi

user = Blueprint('user', __name__)

api = BaseApi(user)
