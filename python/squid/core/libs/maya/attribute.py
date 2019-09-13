# -*- coding: utf-8 -*-
u"""MayaのAttribute関連モジュール"""
from __future__ import absolute_import, division, print_function

# region transform
TRANSLATE_ATTRIBUTES = ["tx", "ty", "tz"]
ROTATION_ATTRIBUTES = ["rx", "ry", "rz"]
SCALE_ATTRIBUTES = ["sx", "sy", "sz"]
TRANSFORM_ATTRIBUTES = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
TRANSLATE = "translate"
ROTATE = "rotate"
# endregion

# region blendshape
INPUT_TARGET = "inputTarget"
WEIGHT = "weight"
# endregion

# region file
FILE_TEXTURE_NAME = "fileTextureName"


# endregion

def convert_attribute(node, attribute):
    u"""対象ノードのアトリビュートに変換して返す

    Args:
        node (unicode): ノード
        attribute (str): アトリビュート

    Returns:
        unicode: 対象ノードのアトリビュート
    """
    return node + "." + attribute
