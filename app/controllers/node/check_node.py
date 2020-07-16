# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.utils import json_success
from .base import api
from ..tasks.corn_check_node import corn_check_node


@api.resource("/check")
class NodeCController(BaseController):
    """节点删除 类"""

    def post(self):
        """ 节点删除 接口
        直接对 redis数据进行删除,然后同步到redis
        POST: /node/remove
        """
        corn_check_node()
        return json_success()
