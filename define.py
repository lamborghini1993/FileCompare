# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-19 14:08:16
@Desc: 一些公共定义
"""
import enum
import os

from PyQt5 import QtCore, QtGui

CACHE_DIR = os.path.join(os.getcwd(), "Cache")


class MODIFICATION(enum.Enum):
    ADD = 1
    DELETE = 2
    MODIFY = 3
    EQUAL = 4


class LINECOLOR(enum.Enum):
    ADD = QtGui.QColor("#d2a980")
    DEL = QtCore.Qt.darkGray
    LMODIFY = QtGui.QColor("#8c93ff")
    RMODIFY = QtGui.QColor("#737bff")
    FILTER = QtGui.QColor("#fff0f1")
    EQUAL = QtCore.Qt.white


class LINEACT(enum.Enum):
    LEFTADD = "minus"
    RIGHTADD = "plus"
    MODIFY = "modify"
    FILTER = "filter"
    NONE = None
