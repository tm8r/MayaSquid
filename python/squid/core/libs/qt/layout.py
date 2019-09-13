# -*- coding: utf-8 -*-
u"""Qtのレイアウト関連"""
from __future__ import absolute_import, division, print_function


def clear_layout(layout):
    u"""指定レイアウトの子をクリア

    Args:
        layout (Qt.QtWidgets.QBoxLayout): 対象のレイアウト
    """
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            else:
                clear_layout(item.layout())
