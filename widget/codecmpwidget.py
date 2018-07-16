# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-11 14:40:43
@Desc: 对比控件
"""

import weakref
import difflib
import re
import copy

from PyQt5 import QtWidgets, QtCore
from . import codewidget


class CCodeEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, *args):
        super(CCodeEdit, self).__init__(*args)
        self.m_BindEditor = None

    def BindBroEditor(self, oEditor):
        if self.m_BindEditor:
            return
        self.m_BindEditor = weakref.ref(oEditor)
        # TODO

    def Load(self, sText):
        pass


class CCodeCmpWidget(QtWidgets.QWidget):
    def __init__(self, *args):
        super(CCodeCmpWidget, self).__init__(*args)
        self.m_LeftSrc = ""
        self.m_RightSrc = ""
        self.m_CmpResult = {}
        self.m_HLayout = QtWidgets.QHBoxLayout(self)
        self.m_LCodeWidget = CCodeEdit()
        self.m_RCodeWidget = CCodeEdit()

        self.m_Splitter = QtWidgets.QSplitter(self)
        self.m_Splitter.addWidget(self.m_LCodeWidget)
        self.m_Splitter.addWidget(self.m_RCodeWidget)
        self.m_HLayout.addWidget(self.m_Splitter)
        self.show()

    def Refersh(self, leftFile, rightFile):
        with open(leftFile, "r") as fp:
            self.m_LeftSrc = fp.read()
        with open(rightFile, "r") as fp:
            self.m_RightSrc = fp.read()
        self.m_CmpResult = {}
        self.CompareByStr()

    def CompareByStr(self):
        differ = difflib.Differ()
        diff = differ.compare(self.m_LeftSrc.splitlines(),
                              self.m_RightSrc.splitlines())
        lstDiff = list(diff)
        dResult = self.m_CmpResult
        iLNum = iRight = 1
        iLRealNum = iRRealNum = 1
        i = 0
        while i < len(lstDiff):
            prefix = lstDiff[i][:2]
            text = lstDiff[i][2:]

            if prefix == "- ":
                dInfo = dResult.setdefault(iLRealNum, {})
                if(i+1 < len(lstDiff) and lstDiff[i+1].startswith("? ")):
                    iLRealNum = iRRealNum = max(iLRealNum, iRRealNum)
                    dInfo = dResult.setdefault(iLRealNum, {})
                    tmp = lstDiff[i+1][2:]
                    dInfo["ldiff"] = [t.start()
                                      for t in re.finditer("\^", tmp)]
                    i += 1
                dInfo["lNum"] = iLNum
                dInfo["lLine"] = text
                iLNum += 1
                iLRealNum += 1

            elif prefix == "+ ":
                dInfo = dResult.setdefault(iRRealNum, {})
                dInfo["rNum"] = iRight
                dInfo["rLine"] = text
                iRight += 1
                iRRealNum += 1
                if(i+1 < len(lstDiff) and lstDiff[i+1].startswith("? ")):
                    tmp = lstDiff[i+1][2:]
                    dInfo["rdiff"] = [t.start()
                                      for t in re.finditer("\^", tmp)]
                    i += 1

            elif prefix == "  ":
                iLRealNum = iRRealNum = max(iLRealNum, iRRealNum)
                dInfo = dResult.setdefault(iRRealNum, {})
                dInfo["lNum"] = iLNum
                dInfo["lLine"] = text
                dInfo["rNum"] = iRight
                dInfo["rLine"] = text
                iLRealNum += 1
                iRRealNum += 1
                iLNum += 1
                iRight += 1

            i += 1
