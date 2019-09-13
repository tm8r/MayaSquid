# -*- coding: utf-8 -*-
u"""ファイル操作関連"""
from __future__ import absolute_import, division, print_function

from squid.vendor.Qt import QtGui

import os

_SIZE_SUFFIXES = ["B", "KB", "MB", "GB", "TB", "PB"]

_FILE_PROTOCOL = "file:///"


def convert_readable_file_size(nbytes):
    u"""HumanReadableなファイルサイズを返す

    Args:
        nbytes (float): ファイルサイズ

    Returns:
        str: HumanReadableなファイルサイズ
    """
    i = 0
    while nbytes >= 1024 and i < len(_SIZE_SUFFIXES) - 1:
        nbytes /= 1024.
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "{0}{1}".format(f, _SIZE_SUFFIXES[i])


def reveal_in_finder(path):
    u"""Finderで指定パスを開く

    Args:
        path (unicode): パス
    """
    QtGui.QDesktopServices.openUrl(_FILE_PROTOCOL + path)


def read_text(path):
    u"""指定されたファイルを読み込んで返す

    Args:
        path (unicode): パス

    Returns:
        unicode: 読込結果
    """
    res = ""
    if not os.path.isfile(path):
        return res
    with open(path, "r") as f:
        res = f.read()
    return res
