# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 09:09'

Usage:

"""
import logging.config

from flask_apscheduler import APScheduler
from flask_redis import FlaskRedis
# Log
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger()

redis = FlaskRedis()

# APScheduler
scheduler = APScheduler()

# SQLAlchemy
db = SQLAlchemy()

# SQLAlchemy Base Model
Base = db.Model

__all__ = [
    "logger",
    "redis",
    "scheduler",
    "Base",
]
