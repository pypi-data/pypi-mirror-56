# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import platform

if platform.system() == 'Windows':
    lib32 = os.path.join(os.path.dirname(__file__), 'cppinterface', 'lib32')
    lib64 = os.path.join(os.path.dirname(__file__), 'cppinterface', 'lib64')
    from glob import glob
    try:
        if ctypes.sizeof(ctypes.c_voidp) == 4:
            dllfile = glob(lib32 + '/*.dll')[0]
        else:
            dllfile = glob(lib64 + '/*.dll')[0]
        ctypes.CDLL(dllfile)
    except:
        pass

sys.path.append(os.path.join(os.path.dirname(__file__), 'cppinterface'))
from amplpython import *
from amplpython import _READTABLE, _WRITETABLE
