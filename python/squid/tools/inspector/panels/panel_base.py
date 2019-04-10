# -*- coding: utf-8 -*-
u"""パネルの基底モジュール"""
from __future__ import absolute_import, division, print_function

from abc import ABCMeta
from abc import abstractmethod

from squid.vendor import six

from squid.vendor.Qt import QtCore
from squid.vendor.Qt import QtWidgets
from squid.vendor.noconflict import classmaker


@six.add_metaclass(classmaker((ABCMeta,)))
class PanelBase(QtWidgets.QFrame):
    u"""パネルの基底クラス"""
    inner_selection_changed = QtCore.Signal(unicode)

    def __init__(self, node_info, parent=None):
        u"""initialize

        Args:
            node_info (squid.tools.inspector.model.NodeInfo): ノード情報
            parent (QtWidgets.QWidget): 親
        """
        super(PanelBase, self).__init__(parent=parent)
        self._node_info = node_info

    @abstractmethod
    def create_ui(self):
        u"""UIを生成"""
        pass

    @abstractmethod
    def is_target(self):
        u"""パネルの生成対象かどうかを返す

        Returns:
            bool: パネルの生成対象かどうか
        """
        return False
