# -*- coding: utf-8 -*-
u"""インスペクタのView"""
from __future__ import absolute_import, division, print_function

from squid.core.libs.maya.layout import delete_window
from squid.core.libs.qt import maya_window
from squid.core.libs.qt.layout import clear_layout
from squid.core.libs.qt.stylesheet import StyleSheet
from squid.tools.inspector import controller
from squid.tools.inspector import panel_factory

from squid.vendor.Qt import QtCore
from squid.vendor.Qt import QtWidgets

from maya import cmds


class Inspector(maya_window.MayaDockableWindow):
    u"""インスペクタのView"""

    _ID = "squid_tools_inspector"

    def __init__(self):
        u"""initialize"""
        super(Inspector, self).__init__()
        self.setWindowTitle("Inspector")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName(self.window_name())
        self.setProperty("saveWindowPref", True)
        self.setStyleSheet(StyleSheet().core_css)
        self.controller = controller.Controller(self)
        self.factory = panel_factory.PanelFactory(self.controller)
        self._create_ui()

    @classmethod
    def open(cls, *args):
        u"""UIを表示"""
        delete_window(cls.window_name())
        if cmds.workspaceControl(cls.workspace_control_name(), ex=True):
            cmds.deleteUI(cls.workspace_control_name())
        win = cls()
        ui_script = cls.ui_script()
        win.show(dockable=True, uiScript=ui_script)

    @classmethod
    def restore(cls, *args):
        u"""workspaceControlをリストア"""
        win = cls()
        win.restore_workspace_parent()

    def _create_ui(self):
        u"""UIを生成"""
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.root_widget = QtWidgets.QFrame(self)
        self.root_widget.setObjectName("root")
        self.setMinimumSize(QtCore.QSize(380, 200))
        self.setCentralWidget(self.root_widget)

        root_layout = QtWidgets.QGridLayout(self.root_widget)
        root_layout.setObjectName("root_layout")
        root_layout.setContentsMargins(8, 8, 8, 8)
        root_layout.setSpacing(0)

        main_widget = QtWidgets.QFrame()
        self.inspector_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(self.inspector_layout)

        tool_content_wrapper = QtWidgets.QScrollArea()
        tool_content_wrapper.setWidget(main_widget)
        tool_content_wrapper.setFrameShape(QtWidgets.QFrame.NoFrame)
        tool_content_wrapper.setWidgetResizable(True)
        tool_content_wrapper.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(tool_content_wrapper, 1, 0, 1, 1)

        self.refresh_inspector_content(self.controller.selected)

    def refresh_inspector_content(self, selected):
        u"""インスペクタのコンテンツを更新

        Args:
            selected (list of unicode): 選択ノードのリスト
        """
        clear_layout(self.inspector_layout)

        if not selected:
            self.inspector_layout.addWidget(QtWidgets.QLabel("No item selected."))
            spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.inspector_layout.addSpacerItem(spacer)
            return

        tab_widget = QtWidgets.QTabWidget()
        self.inspector_layout.addWidget(tab_widget)

        for node in selected:
            frame = QtWidgets.QFrame()
            layout = QtWidgets.QVBoxLayout(frame)

            layout.addWidget(QtWidgets.QLabel("Type: {0}".format(cmds.objectType(node))))
            self.factory.add_panels(node, layout)

            spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            layout.addSpacerItem(spacer)

            tab_widget.addTab(frame, node)

    # override
    def dockCloseEventTriggered(self):
        self.controller.destroy()
