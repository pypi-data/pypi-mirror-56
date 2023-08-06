# !/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------#
# author: sean lee                           #
# email: xmlee97@gmail.com                   #
# -------------------------------------------#

from __future__ import absolute_import, unicode_literals
import sys
from xmnlp.config import path as C_PATH
from . import sentiment

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

model = None

def loader():
    """load model"""
    global model
    if model is None:
        print("(Lazy Load) Loading model...")
        model = sentiment.Sentiment()
        model.load(C_PATH.sentiment['model']['sentiment'])


def predict(text, stopword=None):
    """predict sentiment"""

    loader()
    return model.predict(text, stopword=stopword)


def load(path):
    """load model from path"""

    global model
    model = sentiment.Sentiment()
    model.load(path)
