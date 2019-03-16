# -*- coding: utf-8 -*-
u"""Squid起動モジュール"""
from __future__ import absolute_import, division, print_function

from squid import __title__
from squid import __version__
from squid.core.libs.maya import layout
from squid.tools.inspector.view import Inspector

import maya.cmds as cmds

_MENU_ROOT = "menu_maya_squid"
_SHELF_NAME = "Squid"


class Startup(object):
    u"""Squid起動クラス"""

    @classmethod
    def start(cls, *args):
        u"""最初に呼ばれる"""
        _create_menu()


def _create_menu():
    u"""メニューを作成"""
    cmds.setParent(layout.MAIN_WINDOW)
    cmds.menu(_MENU_ROOT, label=u"Squid", tearOff=True)

    cmds.setParent(_MENU_ROOT, menu=True)
    cmds.menuItem(l="Inspector", c=Inspector.open)

    cmds.menuItem(d=True, p=_MENU_ROOT)
    cmds.menuItem(l=u"Version: {0}({1})".format(__title__, __version__), p=_MENU_ROOT, en=False)
