# -*- coding: utf-8 -*-
u"""BlendShape関連"""
from __future__ import absolute_import, division, print_function

from squid.core.libs.maya import attribute

from maya import cmds


def get_all_blend_shapes():
    u"""シーン上の全てのblendShapeを返す

    Returns:
        list of unicode: blendShapeのリスト
    """
    return cmds.ls(type="blendShape")


def get_input_targets(blend_shape):
    u"""指定blendShapeのinputTargetを返す

    Args:
        blend_shape (unicode): blendShape

    Returns:
        list of unicode: inputTargetのリスト
    """
    if not blend_shape:
        return []
    input_targets = cmds.listConnections(attribute.convert_attribute(blend_shape, attribute.INPUT_TARGET))
    if not input_targets:
        return []
    return input_targets


def get_weight_members(blend_shape):
    u"""指定blendShapeのweightのメンバーを返す

    Args:
        blend_shape (unicode): blendShape

    Returns:
        list of unicode: 指定blendShapeのweightのメンバー
    """
    if not blend_shape:
        return []
    weights = cmds.listAttr(attribute.convert_attribute(blend_shape, attribute.WEIGHT), m=True)
    if not weights:
        return []
    return weights


def get_relative_blend_shapes(target, all_descendents=False, include_self=False):
    u"""指定ノード配下のblendShapeを返す

    Args:
        target (unicode): 対象のノード
        all_descendents (bool): 孫も対象とするかどうか
        include_self (bool): 自身も対象とするかどうか

    Returns:
        list of unicode: 指定ノード配下のblendShapeのリスト
    """
    blend_shapes = []
    if not target:
        return blend_shapes
    transforms = cmds.listRelatives(target, type="transform", ad=all_descendents, f=True)
    if transforms is None:
        transforms = []
    if include_self:
        transforms.append(target)
    for t in transforms:
        tmp_blend_shapes = cmds.ls(cmds.listHistory(t), type="blendShape", long=True)
        if not tmp_blend_shapes:
            continue
        blend_shapes.extend(tmp_blend_shapes)
    return blend_shapes
