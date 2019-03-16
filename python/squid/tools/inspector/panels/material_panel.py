# -*- coding: utf-8 -*-
u"""Materialのパネル"""
from __future__ import absolute_import, division, print_function

from maya import cmds

from squid.core.libs.maya import collector
from squid.core.libs.maya import material
from squid.core.libs.qt.widgets import collapse_widget
from squid.tools.inspector.panels import panel_base

from squid.vendor.Qt import QtWidgets


class MaterialPanel(panel_base.PanelBase):
    u"""Materialのパネル"""

    def __init__(self, node_info):
        u"""initialize

        Args:
            node_info (squid.tools.inspector.model.NodeInfo): ノード情報
        """
        super(MaterialPanel, self).__init__(node_info)
        self._materials = []

    # override
    def create_ui(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(root_layout)

        material_widget = collapse_widget.QCollapseWidget("Materials")
        root_layout.addWidget(material_widget)

        tree_widget = QtWidgets.QTreeWidget()
        tree_widget.setHeaderHidden(True)
        tree_widget.setColumnCount(1)

        tree_widget.itemClicked.connect(self._on_tree_item_clicked)

        material_widget.addWidget(tree_widget)
        for i in xrange(0, len(self._materials)):
            m = self._materials[i]
            mat_item = QtWidgets.QTreeWidgetItem()
            mat_item.setText(0, m)

            tree_widget.insertTopLevelItem(i, mat_item)

            file_nodes = material.get_connected_all_files(m)
            if not file_nodes:
                continue
            for f in file_nodes:
                file_item = QtWidgets.QTreeWidgetItem()
                file_item.setText(0, f)
                mat_item.addChild(file_item)
        tree_widget.expandAll()

    # override
    def is_target(self):
        if not collector.has_shape(self._node_info):
            return False
        histories = cmds.listHistory(self._node_info, future=True, af=True)
        if not histories:
            return False
        self._materials = cmds.ls(cmds.listConnections(histories), mat=True)
        if not self._materials:
            return False
        return True

    def _on_tree_item_clicked(self, current, previous):
        self.inner_selection_changed.emit(current.text(0))
