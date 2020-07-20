# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
create time '2019/8/28 16:27'

Module usage:

docker exec -i sd-python /bin/bash -c 'pytest /home/work/www/fates/fates/tests/test_chart_level_all.py --mysql_env ci'
"""
from copy import deepcopy

from tests.base import TestBase
from tests.test_node.test_node_add import TestNodeAdd


class TestNodeRemove(TestBase):
    """测试 删除节点 接口"""
    path = "/node/remove"
    params = {
        "host": '127.0.0.1',
        "port": 6379,
        "db": 1,
    }

    def test_normal(self, mock_redis_status):
        """
        测试 正常结果

        :return:
        """
        TestNodeAdd().test_normal(mock_redis_status)
        self.send_request(self.path, self.params, 200, 'post', test_id="1.0")

    def test_un_normal(self, mock_redis_status):
        """
        测试 非正常情况
        :param mock_redis_status:
        :return:
        """
        copy_params = deepcopy(self.params)
        copy_params['port'] = 6380
        self.send_request(self.path, copy_params, 500, 'post', test_id="2.0")
