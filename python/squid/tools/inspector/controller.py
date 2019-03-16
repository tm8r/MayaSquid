# -*- coding: utf-8 -*-
u"""コントローラー"""
from __future__ import absolute_import, division, print_function

from squid.vendor.Qt import QtCore

from maya import cmds


class Controller(QtCore.QObject):
    u"""コントローラー"""

    block_changed = QtCore.Signal(bool)
    selection_changed = QtCore.Signal(list)

    def __init__(self, view):
        u"""initialize

        Args:
            view (squid.tools.inspector.view.Inspector): view
        """
        super(Controller, self).__init__()
        self._initialized = False
        self._view = view  # type: squid.tools.inspector.view.Inspector
        self._selected = []
        self._jobs = []
        self._block_refresh = False
        self._create_script_jobs()
        self._connect_signals()
        self._update_selection()
        self._initialized = True

    @property
    def selected(self):
        u"""選択ノードのリストを返す

        Returns:
            list of unicode: 選択ノードのリスト
        """
        return self._selected

    def select_node(self, node):
        u"""ノードを選択

        AttributeEditorやChannelBoxへの適用のための選択なので、InspectorのViewの更新はブロックする

        Args:
            node (unicode): 対象ノード
        """
        self._block_refresh = True
        cmds.select(node)

        # scriptJobの反応が遅いので、Viewの更新のアンブロックを遅延させる
        cmds.evalDeferred(self._unblock_refresh)

    def _create_script_jobs(self):
        self._jobs.append(cmds.scriptJob(e=["SelectionChanged", self._on_selection_changed]))

    def _connect_signals(self):
        self.selection_changed.connect(self._view.refresh_inspector_content)

    def _unblock_refresh(self):
        self._block_refresh = False

    def _on_selection_changed(self):
        if self._block_refresh:
            return
        self._update_selection()

    def _update_selection(self):
        tmp_selected = cmds.ls(sl=True, o=True, st=True)
        selected_dict = dict(zip(tmp_selected[::2], tmp_selected[1::2]))
        res = set()
        for node, node_type in selected_dict.items():
            if node_type == "mesh":
                parents = cmds.listRelatives(node, parent=True)
                if not parents:
                    continue
                res.add(parents[0])
                continue
            res.add(node)

        if not set(self._selected).symmetric_difference(res):
            return

        self._selected = list(res)
        if self._initialized:
            self.selection_changed.emit(self._selected)

    def destroy(self):
        u"""破棄処理"""
        for job in self._jobs:
            if cmds.scriptJob(ex=job):
                cmds.scriptJob(kill=job, force=True)
