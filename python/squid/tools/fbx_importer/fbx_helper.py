# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from squid.vendor.Qt import QtWidgets

from squid.core.libs.maya import fbx
from squid.core.libs.maya import namespace
from squid.tools.fbx_importer import history_helper


def import_fbx(path, import_mode, parent):
    u"""ネームスペース指定でFBXをインポート

    Args:
        path (unicode): パス
        import_mode (squid.core.libs.maya.fbx.FBXImportMode): インポートモード
        parent (QtWidgets.QWidget): 親
    """
    namespaces = namespace.get_namespaces(return_separator=True, return_root=True)

    if len(namespaces) == 1:
        fbx.import_fbx(path, import_mode, namespaces[0])
        history_helper.add_recent_file(path)
        return

    ns, confirmed = QtWidgets.QInputDialog.getItem(parent,
                                                   "Select Namespace",
                                                   u"インポート対象のネームスペースを選択してください。",
                                                   namespaces,
                                                   0,
                                                   False)
    if not confirmed:
        return

    fbx.import_fbx(path, import_mode, ns)
    history_helper.add_recent_file(path)
