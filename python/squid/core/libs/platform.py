# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

_WINDOWS_IDENTIFIER = "nt"


def is_windows():
    return os.name == _WINDOWS_IDENTIFIER
