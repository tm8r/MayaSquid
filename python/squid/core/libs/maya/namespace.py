# -*- coding: utf-8 -*-
u"""ネームスペース関連"""
from __future__ import absolute_import, division, print_function

import os

from maya import cmds

ROOT_NAMESPACE = ":"
_NAMESPACE_SEPARATOR = ":"
_DEFAULT_NAMESPACES = [
    "UI",
    "shared",
    _NAMESPACE_SEPARATOR + "UI",
    _NAMESPACE_SEPARATOR + "shared"
]


def get_namespace_from_path(path):
    u"""ファイルパスからネームスペースを生成して返す

    Args:
        path (unicode): ファイルパス

    Returns:
        unicode: ネームスペース
    """
    return os.path.splitext(os.path.basename(path))[0]


def get_namespace_from_node(node, return_separator=False, return_root=False):
    u"""ノード名からネームスペースを取得して返す

    Args:
        node (unicode): 対象ノード
        return_separator(bool): セパレーターも返すかどうか
        return_root (bool): ルートネームスペースも返すかどうか

    Returns:
        unicode: ネームスペース
    """
    if not node:
        return ""
    node = node.split("|")[-1]

    namespace = ""
    if return_root:
        namespace = ROOT_NAMESPACE
    split = node.rsplit(":", 1)
    if len(split) == 1:
        return namespace
    namespace = split[0]
    if return_separator:
        namespace += _NAMESPACE_SEPARATOR
    return namespace


def is_default_namespace(name):
    u"""デフォルトのネームスペースかどうか判別する."""
    return name in _DEFAULT_NAMESPACES


def get_namespaces(return_separator=False, return_root=False):
    u"""ネームスペースのリストを取得する

    Args:
        return_separator(bool): セパレーターも返すかどうか

    Returns:
        list of unicode: ネームスペースのリスト
    """
    # カレントスペースをルートにリセット
    cmds.namespace(set=ROOT_NAMESPACE)
    namespaces = set()
    if return_root:
        namespaces.add(ROOT_NAMESPACE)
    for sub_namespace in (cmds.namespaceInfo(listOnlyNamespaces=1, recurse=1, an=return_separator)):
        if not is_default_namespace(sub_namespace):
            namespaces.add(sub_namespace)
    return sorted(list(namespaces))


def delete_namespaces(targets=None):
    u"""ネームスペースを削除する

    Args:
        targets (list of unicode): 対象のノードのリスト。指定されていない場合は全ノードを対象にする
    """
    namespaces = get_namespaces()

    # 子(パス名の長いもの)から削除
    namespaces.sort(cmp=lambda s1, s2: cmp(len(s1), len(s2)), reverse=True)
    for x in namespaces:
        if targets is not None and x not in targets:
            continue
        cmds.namespace(removeNamespace=x, mergeNamespaceWithRoot=1)
