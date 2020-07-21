# -*- coding: utf-8 -*-
"""

All rights reserved
create time '2020/7/16 11:08'

Usage:

"""
from zlib import crc32


class ConsistencyHash(object):
    """一致性hash类"""
    def __init__(self, nodes=None, replicas=None):
        """

        :param nodes: 真实节点 list
        :param replicas: 每个真实节点的虚拟节点个数 int
        """
        self.nodes = nodes
        self.replicas = replicas
        self.ring = {}  # key:虚拟节点的hash值 val:真实节点
        self.sorted_keys = []  # 排序之后的虚拟节点的hash值list
        self.add_nodes(nodes)

    def _add_node(self, node):
        """
        添加节点 内部方法
        :param node:
        :return:
        """
        for i in range(self.replicas):
            bnode = "%s_vnode%s" % (node, i)
            bnode = bytes(bnode, encoding="utf8")
            nodehash = abs(crc32(bnode))
            self.ring[nodehash] = node
            self.sorted_keys.append(nodehash)
        self.sorted_keys.sort()
        if node not in self.nodes:
            self.nodes.append(node)

    def add_nodes(self, nodes):
        """
        添加节点
        :param nodes:
        :return:
        """
        if nodes:
            for node in nodes:
                self._add_node(node)

    def remove_nodes(self, nodes):
        """对于remove的操作，如果直接操作已经产生的ring字典，会比较麻烦，因为ring是{hashnode：node}的键值对形式，
        直接处理涉及到字典直接查找值ring.values()/ring.keys()，以及通过值来remove(key)的操作，太麻烦"""
        if nodes:
            for node in nodes:
                for i in range(self.replicas):
                    bnode = "%s_vnode%s" % (node, i)
                    bnode = bytes(bnode, encoding="utf8")
                    nodehash = abs(crc32(bnode))
                    del self.ring[nodehash]
                    self.sorted_keys.remove(nodehash)
                if node in self.nodes:
                    self.nodes.remove(node)

    @property
    def node_info(self):
        """
        获取 环形hash的dict数据
        :return:
        """
        return self.ring
