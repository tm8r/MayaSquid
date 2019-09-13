# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from abc import ABCMeta
from abc import abstractmethod
from squid.vendor import six

_WINDOW_SUFFIX = "_window"
_WORKSPACE_CONTROL_SUFFIX = "WorkspaceControl"

_UI_SCRIPT_FORMAT = """import {0};{0}.{1}.restore()"""

_ID_FORMAT = "{0}.{1}"


def create_window_name(object_id):
    return object_id + _WINDOW_SUFFIX


def create_workspace_control_name(window_id):
    return window_id + _WORKSPACE_CONTROL_SUFFIX


class MayaBaseWindow(object):
    _ID = ""

    @classmethod
    def window_name(cls):
        if cls._ID:
            return create_window_name(cls._ID)
        return create_window_name(cls._get_identifier())

    @classmethod
    def workspace_control_name(cls):
        return create_workspace_control_name(cls.window_name())

    @classmethod
    def ui_script(cls):
        return _UI_SCRIPT_FORMAT.format(cls.__module__, cls.__name__)

    @classmethod
    def _get_identifier(cls):
        return _convert_identifier(cls)


@six.add_metaclass(ABCMeta)
class MayaWindow(MayaBaseWindow):
    def __init__(self):
        super(MayaWindow, self).__init__()

    @classmethod
    @abstractmethod
    def open(cls, *args):
        pass


def _convert_identifier(cls):
    return _ID_FORMAT.format(cls.__module__, cls.__name__)
