# -*- coding: utf-8 -*-
u"""頂点カラーインポートツール"""
from __future__ import absolute_import, division, print_function

import os

from squid.core.libs.maya import blend_shape
from squid.core.libs.maya import decorator
from squid.core.libs.maya import dialog

from maya import cmds
from maya import mel


@decorator.keep_selection
def import_vertex_color(mesh, texture):
    u"""頂点カラーをテクスチャからインポート

    Args:
        mesh (unicode): 対象のMesh
        texture (unicode): 対象のテクスチャパス
    """

    if not os.path.isfile(texture):
        dialog.open_warning_dialog(u"指定されたファイルが見つかりません。")
        return

    cmds.select(cl=True)
    default_ctx = cmds.currentCtx()
    mel.eval("artAttrColorPerVertexToolScript 4;")
    cmds.select(mesh)
    cmds.artAttrPaintVertexCtx(cmds.currentCtx(), e=True, importfileload=texture)
    cmds.setToolTo(default_ctx)

    cmds.select(cl=True)
    cmds.select(mesh, add=True)
    mel.eval('doBakeNonDefHistory( 1, {"prePost"});')

    # ブレンドシェイプのinputTargetsにも頂点カラーが伝播するので削除する
    input_targets = _get_input_targets(mesh)
    if input_targets:
        cmds.select(input_targets)
        cmds.polyColorPerVertex(remove=True)
        for t in input_targets:
            cmds.setAttr(t + ".displayColors", 0)

    dialog.open_in_view_message("Import Color Vertex", u"頂点カラーのインポートが完了しました。")


def _get_input_targets(mesh):
    u"""指定Meshに設定されたブレンドシェイプのinputTargetのリストを返す

    Args:
        mesh (unicode): Mesh

    Returns:
        list of unicode: 指定Meshに設定されたブレンドシェイプのinputTargetのリスト
    """
    res = []
    blend_shapes = blend_shape.get_relative_blend_shapes(mesh, include_self=True)
    if not blend_shapes:
        return res
    return blend_shape.get_input_targets(blend_shapes)
