# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring


class BaseClass(object):
    def __init__(self, _impl):
        self._impl = _impl

    def toString(self):
        return self._impl.toString()

    def __str__(self):
        return self.toString()
