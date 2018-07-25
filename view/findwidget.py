# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-25 10:16:14
@Desc:  查找聊天框
"""

import os
import weakref

from PyQt5 import QtWidgets, QtCore, QtGui
from ui import findwidget_ui

CASW_SENSITIVELY = 1
WHOLE_WORDS = 2
REGULAR = 4


class CFindWidget(QtWidgets.QWidget, findwidget_ui.Ui_Form):
    m_BorderStyleSheet = """
        border-color: #800000;
        border-width: 2px;
        border-style: solid;
    """

    m_StyleSheet = """
        color: #FFFFFF;
        background-color: #7092BE;
        border-style: solid;
    """

    def __init__(self, parent=None):
        super(CFindWidget, self).__init__(parent)
        self.setupUi(self)
        self.hide()
        self.m_Staue = 0
        self.m_Parent = weakref.ref(parent)
        self.InitConnect()

    def InitConnect(self):
        self.pushButton_Pre.clicked.connect(self.FindPre)
        self.pushButton_Next.clicked.connect(self.FindNext)
        self.pushButton_CaseSensitively.clicked.connect(self.E_ChangeCase)
        self.pushButton_WholeWords.clicked.connect(self.E_WholeWords)
        self.pushButton_Regular.clicked.connect(self.E_Regular)

    def Open(self):
        self.show()
        oTxtCursor = self.m_Parent().textCursor()
        sCurWord = str(oTxtCursor.selectedText())
        self.lineEdit.setText(sCurWord)

    def FindPre(self):
        sFindWord = self.lineEdit.text()
        self._FindWords(sFindWord, True)

    def FindNext(self):
        sFindWord = self.lineEdit.text()
        self._FindWords(sFindWord, False)

    def _FindWords(self, sWord, bPre=True):
        """获取匹配选项"""
        document = self.m_Parent().document()
        oBeginCursor = self.m_Parent().textCursor()
        if bPre:
            iFindOpt = QtGui.QTextDocument.FindBackward
        else:
            iFindOpt = QtGui.QTextDocument.FindFlag()

        if(self.m_Staue & CASW_SENSITIVELY):
            iFindOpt |= QtGui.QTextDocument.FindCaseSensitively
        if(self.m_Staue & WHOLE_WORDS):
            iFindOpt |= QtGui.QTextDocument.FindWholeWords
        if(self.m_Staue & REGULAR):
            sWord = QtCore.QRegExp(sWord)
        oNextCursor = document.find(sWord, oBeginCursor, iFindOpt)
        if(not oNextCursor.blockNumber() and not oNextCursor.columnNumber()):   # 可能找到开头，就继续找一次
            oNextCursor = document.find(sWord, oNextCursor, iFindOpt)
        if(oNextCursor.blockNumber() or oNextCursor.columnNumber()):   # 第二次没找到说明不存在
            self.m_Parent().setTextCursor(oNextCursor)
            self.m_Parent().centerCursor()

    def E_ChangeCase(self):
        """切换大小写敏感"""
        self.m_Staue ^= CASW_SENSITIVELY
        self._PushButtonChangeColor(self.pushButton_CaseSensitively, self.m_Staue & CASW_SENSITIVELY)

    def E_WholeWords(self):
        """切换全字匹配"""
        self.m_Staue ^= WHOLE_WORDS
        self._PushButtonChangeColor(self.pushButton_WholeWords, self.m_Staue & WHOLE_WORDS)

    def E_Regular(self):
        """切换正则匹配"""
        self.m_Staue ^= REGULAR
        self._PushButtonChangeColor(self.pushButton_Regular, self.m_Staue & REGULAR)

    def _PushButtonChangeColor(self, oBtn, bBorder):
        if bBorder:
            oBtn.setStyleSheet(self.m_BorderStyleSheet)
        else:
            oBtn.setStyleSheet(self.m_StyleSheet)

    def keyPressEvent(self, event):
        if(event.modifiers() == QtCore.Qt.AltModifier):
            if(event.key() == QtCore.Qt.Key_C):
                self.E_ChangeCase()
            if(event.key() == QtCore.Qt.Key_W):
                self.E_WholeWords()
            if(event.key() == QtCore.Qt.Key_R):
                self.E_Regular()
        if(event.modifiers() == QtCore.Qt.ShiftModifier):
            if(event.key() == QtCore.Qt.Key_F3):
                self.FindPre()
        if(event.key() == QtCore.Qt.Key_F3):
            self.FindNext()
