# -*- coding: utf-8 -*-
u"""コンストレイントのパネル"""
from __future__ import absolute_import, division, print_function

from squid.core.libs.maya import constraint
from squid.core.libs.qt.widgets import collapse_widget
from squid.tools.inspector.panels import panel_base

from squid.vendor.Qt import QtCore
from squid.vendor.Qt import QtWidgets

from maya import cmds


class ConstraintPanel(panel_base.PanelBase):
    u"""コンストレイントのパネル"""

    def __init__(self, node_info):
        u"""initialize

        Args:
            node_info (squid.tools.inspector.model.NodeInfo): ノード情報
        """
        super(ConstraintPanel, self).__init__(node_info)
        self._constraints = []
        self._rconstraints = []

    # override
    def create_ui(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(root_layout)

        const_widget = collapse_widget.QCollapseWidget("Constraints")
        root_layout.addWidget(const_widget)
        tree_widget = QtWidgets.QTreeWidget()
        tree_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        tree_widget.setIndentation(0)
        tree_widget.setHeaderHidden(True)
        tree_widget.setColumnCount(2)
        tree_widget.hideColumn(1)
        tree_widget.itemClicked.connect(self._on_tree_item_clicked)
        const_widget.addWidget(tree_widget)
        if self._constraints:
            for const_type, members in self._constraints.items():
                for m in members:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setText(0, "<- {0}({1})".format(cmds.ls(m)[0], const_type.name))
                    item.setText(1, m)
                    tree_widget.insertTopLevelItem(tree_widget.topLevelItemCount(), item)
        if self._rconstraints:
            for const_type, members in self._rconstraints.items():
                for m in members:
                    item = QtWidgets.QTreeWidgetItem()
                    item.setText(0, "-> {0}({1})".format(cmds.ls(m)[0], const_type.name))
                    item.setText(1, m)
                    tree_widget.insertTopLevelItem(tree_widget.topLevelItemCount(), item)

    # override
    def is_target(self):
        self._constraints = constraint.get_constraint_members_dict(self._node_info)
        self._rconstraints = constraint.get_constraint_members_dict_reverse(self._node_info)
        if not self._constraints and not self._rconstraints:
            return False
        return True

    def _on_tree_item_clicked(self, current, previous):
        self.inner_selection_changed.emit(current.text(1))
