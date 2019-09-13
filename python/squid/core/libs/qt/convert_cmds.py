# -*- coding: utf-8 -*-
u"""QtとMayaのUIの変換"""
from __future__ import absolute_import, division, print_function

from squid.vendor.Qt import QtCompat
from squid.vendor.Qt import QtWidgets
from squid.vendor.Qt import QtCore

from maya import OpenMayaUI as omui


def convert_to_qt_instance(name):
    u"""cmdsで作成したUIをQtで利用可能なインスタンスとして返す

    Args:
        name (unicode): cmdsで作成したUIの名前

    Returns:
        Qt.QtWidgets.QWidget: Qtで利用可能なインスタンス
    """
    ptr = omui.MQtUtil.findControl(name)
    if not ptr:
        ptr = omui.MQtUtil.findLayout(name)
        if ptr is None:
            ptr = omui.MQtUtil.findMenuItem(name)
    return QtCompat.wrapInstance(long(ptr), QtWidgets.QWidget)


def convert_to_cmds(q_object):
    return omui.MQtUtil.fullName(long(QtCompat.getCppPointer(q_object)))
