# !/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------#
# author: sean lee                           #
# email: xmlee97@gmail.com                   #
# -------------------------------------------#

from __future__ import absolute_import, unicode_literals
import sys
from xmnlp.config import path as C_PATH
from .radical import Radical

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

model = None

def loader():
    """load model"""
    global model
    if model is None:
        print("(Lazy Load) Loading model...")
        model = Radical()
        model.load(C_PATH.radical['model']['radical'])


def radical(text):
    """获取偏旁"""

    loader()
    if not text:
        return None
    return [model.radical(ch) for ch in text]
