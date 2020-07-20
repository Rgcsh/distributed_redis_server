# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.controllers.tasks.corn_check_node import corn_check_node
from app.utils import json_success
from .base import api


@api.resource("/check")
class NodeCController(BaseController):
    """节点检查 类"""

    def post(self):
        """ 节点检查 接口
        POST: /node/check
        """
        corn_check_node()
        return json_success()
