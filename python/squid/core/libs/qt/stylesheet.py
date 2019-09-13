# -*- coding: utf-8 -*-
u"""スタイルシート"""
from __future__ import absolute_import, division, print_function

import os
from squid.vendor import six

from squid.core.libs.files import read_text
from squid.core.libs.singleton import SingletonType

_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")


@six.add_metaclass(SingletonType)
class StyleSheet(object):
    u"""スタイルシート管理"""

    _CSS_DICT = {}

    def __init__(self):
        u"""initialize"""
        self._core_css = read_text(_RESOURCES_DIRECTORY + "/core.css")

    @property
    def core_css(self):
        u"""共通CSSを返す

        Returns:
            str: 共通CSS
        """
        return self._core_css

    def get_css(self, path):
        u"""共通CSSとツールごとのCSSをマージして返す

        Args:
            path (unicode): ツールごとのCSSのパス

        Returns:
            unicode: 共通CSSとツールごとのCSSのマージ結果
        """
        if path not in self._CSS_DICT:
            self._CSS_DICT[path] = read_text(path)
        return self._core_css + self._CSS_DICT[path]

    def reload(self):
        u"""CSSをリロード（開発用）"""
        self._core_css = read_text(_RESOURCES_DIRECTORY + "/core.css")
        self._CSS_DICT = {}
