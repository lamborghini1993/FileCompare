# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-19 14:08:16
@Desc: 一些公共定义
"""
import enum

from PyQt5 import QtCore, QtGui

TEST_FILE1 = r"E:\mygithub\FileCompare\test\py2ui.py"
TEST_FILE2 = r"E:\mygithub\FileCompare\test\py2ui2.py"


class MODIFICATION(enum.Enum):
    ADD = 1
    DELETE = 2
    MODIFY = 3
    EQUAL = 4


class LINECOLOR(enum.Enum):
    ADD = QtGui.QColor("#d2a980")
    DEL = QtCore.Qt.darkGray
    RMODIFY = QtGui.QColor("#aaaaf0")
    LMODIFY = QtGui.QColor("#faa755")
    EQUAL = QtCore.Qt.white


class LINEACT(enum.Enum):
    LEFTADD = "minus"
    RIGHTADD = "plus"
    MODIFY = "modify"
    NONE = None
