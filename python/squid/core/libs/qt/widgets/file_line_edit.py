# -*- coding: utf-8 -*-
u"""ファイルをD&D可能なQLineEdit"""
from __future__ import absolute_import, division, print_function

from squid.vendor.Qt import QtWidgets


class QFileLineEdit(QtWidgets.QLineEdit):
    u"""ファイルをD&D可能なQLineEdit"""

    def __init__(self, parent=None):
        super(QFileLineEdit, self).__init__(parent=parent)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if _is_file(event.mimeData()):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if _is_file(event.mimeData()):
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if not _is_file(mime_data):
            return
        path = _get_path(mime_data)
        if not path:
            return
        self.setText(path)


def _is_file(mime_data):
    urls = mime_data.urls()
    if not urls:
        return False
    return urls[0].scheme() == "file"


def _get_path(mime_data):
    if not _is_file:
        return None
    urls = mime_data.urls()
    return urls[0].path()[1:]
