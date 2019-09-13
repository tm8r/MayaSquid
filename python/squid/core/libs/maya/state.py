# -*- coding: utf-8 -*-
u"""Mayaの状態関連モジュール"""
from __future__ import absolute_import, division, print_function

from maya import cmds

VERSION = int(cmds.about(v=True)[:4])


def is_enable_workspace_control():
    u"""workspaceControl対応バージョンかどうかを返す

    Returns:
        bool: workspaceControl対応バージョンかどうか
    """
    return VERSION > 2016
