# -*- coding: utf-8 -*-
u"""モデル"""
from __future__ import absolute_import, division, print_function


class NodeInfo(object):
    u"""ノード情報"""

    def __init__(self, node):
        u"""initialize

        Args:
            node (unicode): ノード
        """
        self._node = node

    @property
    def node(self):
        u"""ノード名を返す

        Returns:
            unicode: ノード名
        """
        return self._node
