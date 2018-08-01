# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-27 10:30:37
@Desc: 
"""
import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui

FILE = r"./../test/py2ui.txt"


class CMyText(QtWidgets.QPlainTextEdit):
    m_Start = 10
    m_End = 50

    def __init__(self, parent=None):
        super(CMyText, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        with open(FILE, "r", encoding="utf8") as fp:
            lstLines = fp.readlines()
            lst = []
            for i, line in enumerate(lstLines):
                lst.append("%s-%s" % (i, line)) # 添加行号，方便直观观察
            self.setPlainText("".join(lst))

    def E_Fold(self):
        document = self.document()
        for x in range(self.m_Start + 1, self.m_End + 1):
            oTextBlock = document.findBlockByNumber(x)
            oTextBlock.setVisible(False)
        self.viewport().update()
        document.adjustSize()

    def E_Unfold(self):
        document = self.document()
        for x in range(self.m_Start + 1, self.m_End + 1):
            oTextBlock = document.findBlockByNumber(x)
            oTextBlock.setVisible(True)
        self.viewport().update()
        document.adjustSize()

    def scrollContentsBy(self, dx, dy):
        self.viewport().update()
        super(CMyText, self).scrollContentsBy(dx, dy)
