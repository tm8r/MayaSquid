# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class SingletonType(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)

        return cls._instance
