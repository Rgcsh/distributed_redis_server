# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/6 14:48'

Usage:

"""

from app.controllers.base import BaseController
from app.models.distributed_redis_server_db.server_info import ServerInfoModel
from app.utils import json_success
from .base import api


@api.resource("/master_server_list")
class ServerInfoMasterServerListController(BaseController):
    """获取主服务器 相关信息"""

    def get(self):
        """
        POST: /server_info/master_server_list
        """
        result = ServerInfoModel.get_master_server_info()
        return json_success(result)
