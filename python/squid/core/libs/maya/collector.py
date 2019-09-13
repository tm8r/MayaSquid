# -*- coding: utf-8 -*-
u"""ノード収集関連"""
from __future__ import absolute_import, division, print_function

from logging import getLogger

from maya import cmds

_SELECTION_MASK_POLYGON = 12

logger = getLogger(__name__)


def get_short_name(full_path):
    u"""フルパスからショートネームを取得

    Args:
        full_path (unicode): フルパス

    Returns:
        unicode: ショートネーム
    """
    return full_path.split("|")[-1]


def get_short_name_without_namespace(full_path):
    u"""フルパスからネームスペースを除外したショートネームを取得

    Args:
        full_path (unicode): フルパス

    Returns:
        unicode: ショートネーム
    """
    return get_short_name(full_path).split(":")[-1]


def get_child_transforms_has_shape(node):
    u"""指定ノード配下のshapeを持つtransformを全て返す

    Args:
        node (unicode): 対象のノード

    Returns:
        list of unicode: 指定ノード配下のshapeを持つtransformのリスト
    """
    res = []
    shapes = cmds.filterExpand(cmds.listRelatives(node, f=True, type="transform"), sm=_SELECTION_MASK_POLYGON)
    if shapes:
        res.extend(shapes)
    return res


def get_child_shapes(node):
    u"""指定ノード配下のshapeを全て返す

    Args:
        node (unicode or list of unicode): 対象のノード

    Returns:
        list of unicode: 指定ノード配下のshapeのリスト
    """
    res = []
    transforms = get_child_transforms_has_shape(node)
    if not transforms:
        return res
    for t in transforms:
        res.extend(cmds.listRelatives(t, s=True, ni=True))
    return res


def get_child_joints(node, all_descendents=True):
    u"""指定ノード配下のjointを全て返す

    Args:
        node (unicode or list of unicode): 対象のノード
        all_descendents (bool): 子孫全てを取得

    Returns:
        list of unicode: 指定ノード配下のjointのリスト
    """
    res = []
    joints = cmds.listRelatives(node, ad=all_descendents, f=True, type="joint")
    if joints:
        res.extend(joints)
    return res


def get_child_locators(node, all_descendents=True):
    u"""指定ノード配下のロケーターを全て返す

    Args:
        node (unicode or list of unicode): 対象のノード
        all_descendents (bool): 子孫全てを取得

    Returns:
        list of unicode: 指定ノード配下のロケーターのリスト
    """
    res = []
    if all_descendents:
        locators = cmds.listRelatives(node, ad=all_descendents, f=True, type="locator", ni=True, s=False)
        if not locators:
            return res
        res.extend(cmds.listRelatives(locators, f=True, p=True))
    else:
        # all_descendentsがFalseの場合、locatorはlistRelativesでtransformを起点に実行しないと返ってこないので、
        # 先にtransformを取得する
        transforms = cmds.listRelatives(node, ad=all_descendents, f=True, type="transform", ni=True, s=False)
        if not transforms:
            return res
        # 返ってくるlocatorはShapeなので、locatorを子に持つtransformを返す
        res.extend([x for x in transforms if cmds.listRelatives(x, f=True, type="locator", ni=True, s=False)])

    return res


def get_child_joints_and_locators(node, all_descendents=True):
    u"""指定ノード配下のjointとロケーターを全て返す

    Args:
        node (unicode or list of unicode): 対象のノード
        all_descendents (bool): 子孫全てを取得

    Returns:
        list of unicode: 指定ノード配下のjointとロケーターのリスト
    """
    res = []
    res.extend(get_child_joints(node, all_descendents=all_descendents))
    res.extend(get_child_locators(node, all_descendents=all_descendents))
    return res


def is_parent(parent, child, allows_hierarchy_count=-1):
    u"""指定したノードが親子（孫）関係にあるかどうかを返す

    Args:
        parent (unicode): 親ノード
        child (unicode): 子ノード
        allows_hierarchy_count(int): 許容する階層数（指定しなければ無限）

    Returns:
        bool: 指定したノードが親子（孫）関係にあるかどうか
    """
    tmp_parent = cmds.ls(parent, long=True)
    if len(tmp_parent) > 1:
        logger.error("invalid parent number")
        return False
    parent = tmp_parent[0]
    tmp_child = cmds.ls(child, long=True)
    if len(tmp_child) > 1:
        logger.error("invalid child number")
        return False
    child = tmp_child[0]
    res = any([x for x in cmds.listRelatives(parent, ad=True, ni=True, f=True) if x == child])

    if not res:
        return False

    if allows_hierarchy_count <= 0:
        return True
    hierarchy_count_diff = len(child.split("|")) - len(parent.split("|"))
    return hierarchy_count_diff <= allows_hierarchy_count


def get_root(node):
    u"""ルートを取得

    Args:
        node (unicode): 対象のノード

    Returns:
        unicode: ルートノード
    """
    root = node
    while node:
        node = cmds.listRelatives(node, f=True, p=True)
        if node:
            root = node[0]
    return cmds.ls(root)[0]


def is_group(node):
    u"""指定ノードがグループノードかどうかを返す

    Args:
        node (unicode): 対象のノード

    Returns:
        bool: 指定ノードがグループノードかどうか
    """
    if cmds.nodeType(node, api=True) != "kTransform":
        return False
    return not cmds.listRelatives(node, s=True, f=True)


def has_shape(node):
    u"""指定ノードがシェイプを持つノードかどうかを返す

    Args:
        node (unicode): 対象のノード

    Returns:
        bool: 指定ノードがシェイプを持つノードかどうか
    """
    children = cmds.listRelatives(node, f=True, s=True)
    if not children:
        return False
    return len([x for x in children if cmds.nodeType(x) == "mesh"]) > 0
