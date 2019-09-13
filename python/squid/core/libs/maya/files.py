# -*- coding: utf-8 -*-
u"""Mayaファイル操作関連"""
from __future__ import absolute_import, division, print_function

import os

from maya import cmds
from maya import mel

from squid.core.libs.platform import is_windows

SCENE_DIRECTORY = "scenes"
SOURCE_IMAGES_DIRECTORY = "sourceimages"

_SIZE_SUFFIXES = ["B", "KB", "MB", "GB", "TB", "PB"]

_FILE_TYPES = {".ma": "mayaAscii", ".mb": "mayaBinary", ".fbx": "FBX", ".obj": "OBJ"}

_MAYA_PATH_SEPARATOR = "/"


def get_scene_path():
    u"""現在開いているシーンのパスを返す

    Returns:
        unicode: 現在開いているシーンのパス
    """
    return cmds.file(q=True, sn=True)


def open_file(path, add_recent=True, set_project=True):
    u"""ファイルを開く

    Args:
        path (unicode): パス
        add_recent (bool): 最近開いたファイルに追加するかどうか
        set_project (bool): セットプロジェクトを行うかどうか
    """
    cmds.file(new=True, force=True)
    cmds.file(path, o=True, force=True)

    if add_recent:
        mel.eval('addRecentFile("' + path + '", "' + get_file_type(path) + '");')

    if set_project:
        # 親ディレクトリがscenesの場合はセットプロジェクトを行う
        parent_dir = os.path.basename(os.path.dirname(path))
        if parent_dir != SCENE_DIRECTORY:
            return
        project_dir = os.path.dirname(os.path.dirname(path))
        mel.eval('setProject "' + project_dir + '";')


def get_file_type(path):
    u"""ファイルタイプを返す

    Args:
        path (unicode): パス

    Returns:
        str: ファイルタイプ
    """
    _, ext = os.path.splitext(path)
    return _FILE_TYPES.get(ext, "")


def from_native_path(path):
    u"""OSごとのパス表現をMayaのパス表現に変換する（MELのfromNativePathと同義）

    Args:
        path (unicode): パス

    Returns:
        unicode: パス
    """
    if not is_windows():
        return path
    return path.replace(os.path.sep, _MAYA_PATH_SEPARATOR)


def save_changes():
    u"""シーンを保存する

    Returns:
        bool: キャンセルをした場合はFalse、それ以外（保存、保存しないを選択した場合はTrue）
    """
    res = mel.eval('saveChanges("");')
    if res == 0:
        return False
    return True
