# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
create time '2019/8/28 16:27'

Module usage:

docker exec -i sd-python /bin/bash -c 'pytest /home/work/www/fates/fates/tests/test_chart_level_all.py --mysql_env ci'
"""

from tests.base import TestBase
from tests.test_node.test_node_add import TestNodeAdd


class TestNodeCheck(TestBase):
    """测试  接口"""
    path = "/node/check"
    params = {
    }

    def test_normal(self, mock_redis_status):
        """
        测试 正常结果

        :return:
        """
        TestNodeAdd().test_normal(mock_redis_status)
        self.send_request(self.path, self.params, 200, 'post', test_id="1.0")
