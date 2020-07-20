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


class TestNodeAdd(TestBase):
    """测试  接口"""
    path = "/node/add"
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
        self.del_map()
        self.send_request(self.path, self.params, 200, 'post', test_id="1.0")

    def test_params(self, mock_redis_status):
        """
        测试 参数是否正确
        :return:
        """
        self.del_map()

        # db参数值大小限制
        copy_params = deepcopy(self.params)
        copy_params['db'] = 0
        copy_params['port'] = 6385
        self.send_request(self.path, copy_params, 200, 'post', test_id="2.1")

        copy_params = deepcopy(self.params)
        copy_params['db'] = -1
        copy_params['port'] = 6387
        self.send_request(self.path, copy_params, 571, 'post', test_id="2.2")

        copy_params = deepcopy(self.params)
        copy_params['db'] = 15
        copy_params['port'] = 6386
        self.send_request(self.path, copy_params, 200, 'post', test_id="2.3")

        copy_params = deepcopy(self.params)
        copy_params['db'] = 16
        self.send_request(self.path, copy_params, 573, 'post', test_id="2.4")

        # 节点冲突
        copy_params = deepcopy(self.params)
        copy_params['db'] = 15
        self.send_request(self.path, copy_params, 500, 'post', test_id="2.4")

    def test_unconnect(self):
        """
        测试节点无法连接
        :return:
        """
        copy_params = deepcopy(self.params)
        copy_params['port'] = 6390
        self.send_request(self.path, copy_params, 500, 'post', test_id="2.4")
