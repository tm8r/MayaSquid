# -*- coding: utf-8 -*-
u"""Qt用MayaWindow基底モジュール"""
from __future__ import absolute_import, division, print_function

from abc import ABCMeta
from abc import abstractmethod
from squid.vendor.noconflict import classmaker
from squid.vendor.Qt import QtCompat
from squid.vendor.Qt import QtCore
from squid.vendor.Qt import QtWidgets
from squid.vendor import six

from squid.core.libs.maya.maya_window import MayaBaseWindow

from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

try:
    MAYA_WINDOW = QtCompat.wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
except:
    MAYA_WINDOW = None


class MayaWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow, MayaBaseWindow):
    u"""Qt用MayaWindow基底クラス"""

    def __init__(self, parent=MAYA_WINDOW):
        u"""initialize

        Args:
            parent (Qt.QtWidgets.QWidget): parent
        """
        super(MayaWindow, self).__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    @classmethod
    def open(cls, *args):
        u"""ウィンドウを開く"""
        pass


@six.add_metaclass(classmaker((ABCMeta,)))
class MayaDockableWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow, MayaBaseWindow):
    u"""Qt用MayaWindow基底クラス（workspaceControl使用）"""

    def __init__(self, *args, **kwargs):
        u"""initialize

        Args:
            parent (Qt.QtWidgets.QWidget): parent
        """
        super(MayaDockableWindow, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    @classmethod
    @abstractmethod
    def open(cls, *args):
        u"""ウィンドウを開く"""
        pass

    @classmethod
    @abstractmethod
    def restore(cls, *args):
        u"""workspaceControlをリストア"""
        pass

    def restore_workspace_parent(self):
        parent = omui.MQtUtil.getCurrentParent()
        mixin_ptr = omui.MQtUtil.findControl(self.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(parent))


@six.add_metaclass(classmaker((ABCMeta,)))
class MayaView(MayaQWidgetBaseMixin, QtWidgets.QMainWindow, MayaBaseWindow):
    u"""Qt用MayaView基底クラス（Presenter利用時に使用する）"""

    def __init__(self, parent=MAYA_WINDOW):
        u"""initialize

        Args:
            parent (Qt.QtWidgets.QWidget): parent
        """
        super(MayaView, self).__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
