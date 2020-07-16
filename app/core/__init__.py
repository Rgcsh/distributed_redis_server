# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
import logging.config

from flask_apscheduler import APScheduler
from flask_redis import FlaskRedis

__all__ = [
    "logger",
    "redis",
    "scheduler",
]

# Log
logger = logging.getLogger()

redis = FlaskRedis()

# APScheduler
scheduler = APScheduler()
