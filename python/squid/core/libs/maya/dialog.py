# -*- coding: utf-8 -*-
u"""Mayaダイアログ"""
from __future__ import absolute_import, division, print_function

import os

from maya import cmds


def open_error_dialog(message):
    u"""結果を返さないエラーダイアログを表示

    Args:
        message (unicode):メッセージ
    """
    _open_message_dialog("Error", message)


def open_warning_dialog(message):
    u"""結果を返さない警告ダイアログを表示

    Args:
        message (unicode):メッセージ
    """
    _open_message_dialog("Warning", message)


def open_information_dialog(message):
    u"""結果を返さない情報ダイアログを表示

    Args:
        message (unicode):メッセージ
    """
    _open_message_dialog("Information", message)


def _open_message_dialog(title, message):
    u"""結果を返さないダイアログを表示

    Args:
        title (unicode): タイトル
        message (unicode): メッセージ
    """
    cmds.confirmDialog(t=title, m=message)


def open_in_view_message(title, message, pos="topRight", fade=True, fade_stay_time=5000):
    u"""inViewMessageを表示

    Args:
        title (unicode): タイトル
        message (unicode): メッセージ
        pos (unicode): 表示位置
        fade (bool): フェードするかどうか
        fade_stay_time (int): メッセージ表示時間（ミリ秒）
    """
    cmds.inViewMessage(amg=u"<font color='#00b4ee'>{0}</font>{1}{2}".format(title, os.linesep, message),
                       pos=pos,
                       fade=fade,
                       fst=fade_stay_time)


def open_confirm_dialog(message, title="Confirm"):
    u"""確認ダイアログを表示

    Args:
        message (unicode): メッセージ
        title (unicode): タイトル

    Returns:
        bool: ユーザーが許可したかどうか
    """
    confirmed = cmds.confirmDialog(t=title,
                                   m=message,
                                   button=["Yes", "No"],
                                   defaultButton="Yes",
                                   cancelButton="No",
                                   dismissString="No")
    return confirmed == "Yes"
