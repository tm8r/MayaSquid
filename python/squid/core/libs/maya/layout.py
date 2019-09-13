# -*- coding: utf-8 -*-
u"""レイアウト関連"""
from __future__ import absolute_import, division, print_function

from squid.core.libs.maya import state

from maya import cmds

MAIN_WINDOW = "MayaWindow"


def delete_window(window, *args):
    u"""既に存在するウィンドウを削除する

    Args:
        window (unicode): ウィンドウ名
    """
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)


def delete_workspace_control(workspace_control, *args):
    u"""既に存在するworkspaceControlを削除する

    Args:
        workspace_control (unicode): workspaceControl名
    """
    if not state.is_enable_workspace_control():
        return
    if cmds.workspaceControl(workspace_control, ex=True):
        cmds.deleteUI(workspace_control)
