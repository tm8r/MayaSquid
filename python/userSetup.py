# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.utils


def startup():
    u"""ツール起動"""
    try:
        from squid import startup
        startup.Startup.start()
    except:
        import traceback
        print(traceback.format_exc())


maya.utils.executeDeferred(startup)
