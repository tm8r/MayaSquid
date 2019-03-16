# -*- coding: utf-8 -*-
u"""パネル管理モジュール"""
from __future__ import absolute_import, division, print_function

from squid.tools.inspector.panels import blend_shape_panel
from squid.tools.inspector.panels import constraint_panel
from squid.tools.inspector.panels import material_panel

_PANELS = [
    material_panel.MaterialPanel,
    blend_shape_panel.BlendShapePanel,
    constraint_panel.ConstraintPanel,
]


class PanelFactory(object):
    u"""Panelの管理クラス"""

    def __init__(self, controller):
        u"""initialize

        Args:
            controller (squid.tools.inspector.controller.Controller): controller
        """
        self.panels = _PANELS
        self._controller = controller

    def add_panels(self, node, layout):
        u"""パネルを追加

        Args:
            node (unicode): 対象ノード
            layout (Qt.QtWidgets.QBoxLayout): レイアウト
        """
        for p in self.panels:
            panel = p(node)
            if not panel.is_target():
                continue

            panel.create_ui()
            panel.inner_selection_changed.connect(self._controller.select_node)
            layout.addWidget(panel)
