# !/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------#
# author: sean lee                           #
# email: xmlee97@gmail.com                   #
# -------------------------------------------#

from __future__ import absolute_import, unicode_literals
import sys
from xmnlp.config import path as C_PATH
from xmnlp.config import regx as R
from xmnlp.postag import seg
from .checker import Checker

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
elif sys.version_info[0] == 3:
    unicode = str

# checker model
model = None

def loader():
    """load model"""
    global model
    if model is None:
        print("(Lazy Load) Loading model...")
        model = Checker()

def set_userdict(fpath):
    """set user dict"""
    loader()
    model.userdict(fpath)

def check(doc, level=0):
    """check doc

    Args:
      level:
        - 0: word
        - 1: doc
    """
    loader()
    if isinstance(doc, (str, unicode)):
        if level == 0:
            return model.best_match(doc)
        return model.doc_checker(doc)
    raise ValueError('Error [Chekcer]: invalid input type, str is required!')
