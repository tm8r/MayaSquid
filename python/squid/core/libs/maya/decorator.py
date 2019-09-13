# -*- coding: utf-8 -*-
u"""Maya関連デコレーター"""
from __future__ import absolute_import, division, print_function

import functools
import sys

from maya import cmds


def undoable(func):
    u"""UndoChunkをまとめるデコレーター"""

    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            et, ei, tb = sys.exc_info()
            raise Exception, Exception(e), tb
        finally:
            cmds.undoInfo(closeChunk=True)

    return wrapper


def keep_selection(f):
    u"""選択を保持するデコレーター"""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            tmp_selection = cmds.ls(sl=True, l=True)
            result = f(*args, **kwargs)
            try:
                cmds.select(tmp_selection)
            except:
                pass

            return result
        except Exception:
            raise

    return wrapper
