# -*- coding: utf-8 -*-
u"""FBX関連"""
from __future__ import absolute_import, division, print_function

from logging import getLogger
import os

from squid.core.libs.maya import namespace
from squid.vendor.enum import Enum

from maya import cmds

FBX_EXTENSION = ".fbx"

logger = getLogger(__name__)


class FBXImportMode(Enum):
    u"""FBXのインポートのモード"""

    __order__ = "Add Merge ExMerge"
    Add = "Add"
    Merge = "Merge"
    ExMerge = "Exmerge"


def load_fbx_plugin():
    u"""FBXプラグインを読み込み"""
    if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
        cmds.loadPlugin("fbxmaya")
        cmds.pluginInfo("fbxmaya", e=True, autoload=True)


def import_fbx(path, mode=FBXImportMode.Add, ns=""):
    u"""FBXをインポート

    Args:
        path (unicode): FBXのパス
        mode (FBXImportMode): インポートモード
        ns (unicode): ネームスペース
    """
    _, ext = os.path.splitext(path)
    if ext != FBX_EXTENSION:
        logger.error(u"Invalid extension. path={0}".format(path))
        return
    load_fbx_plugin()
    cmds.FBXImportMode("-v", mode.value)
    cmds.FBXImportMergeAnimationLayers("-v", True)
    cmds.FBXImportLights("-v", False)
    cmds.FBXImportConstraints("-v", False)
    if ns and ns != namespace.ROOT_NAMESPACE:
        # ネームスペース指定の場合はfileコマンドからFBXImportを実行する
        try:
            cmds.namespace(set=ns)
            cmds.file(path, i=True, type="FBX", iv=True, ra=True, mnc=True, pr=True, itr="combine", ns=ns)
        finally:
            cmds.namespace(set=namespace.ROOT_NAMESPACE)
    else:
        cmds.FBXImport("-f", path)
