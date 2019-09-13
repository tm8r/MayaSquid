# -*- coding: utf-8 -*-
u"""履歴管理"""
from __future__ import absolute_import, division, print_function

from maya import cmds

_RECENT_FILES_KEY = "squid_recent_fbx_files"
_RECENT_FILES_LIMIT = 10


def get_recent_files():
    u"""最近使用したファイルリストを返す

    Returns:
        list of unicode: 最近使用したファイルリスト
    """
    if not cmds.optionVar(ex=_RECENT_FILES_KEY):
        return []
    res = list(cmds.optionVar(q=_RECENT_FILES_KEY))
    res.reverse()
    return res


def add_recent_file(path):
    u"""指定ファイルを履歴に追加

    Args:
        path (unicode): パス
    """
    if not path:
        return
    if cmds.optionVar(ex=_RECENT_FILES_KEY):
        files = cmds.optionVar(q=_RECENT_FILES_KEY)

        for i in xrange(0, len(files)):
            if path == files[i]:
                cmds.optionVar(rfa=(_RECENT_FILES_KEY, i))
                break
    cmds.optionVar(sva=(_RECENT_FILES_KEY, path))

    files = cmds.optionVar(q=_RECENT_FILES_KEY)

    if len(files) <= _RECENT_FILES_LIMIT:
        return

    for i in xrange(0, len(files) - _RECENT_FILES_LIMIT):
        cmds.optionVar(rfa=(_RECENT_FILES_KEY, 0))
