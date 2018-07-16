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
        self.m_HLayout = QtWidgets.QHBoxLayout(self)
        self.m_LCodeWidget = CCodeEdit()
        self.m_RCodeWidget = CCodeEdit()

        self.m_Splitter = QtWidgets.QSplitter(self)
        self.m_Splitter.addWidget(self.m_LCodeWidget)
        self.m_Splitter.addWidget(self.m_RCodeWidget)
        self.m_HLayout.addWidget(self.m_Splitter)
        self.show()

    def Refersh(self, file1, file2):
        with open(file1, "r") as fp:
            self.m_Str1 = fp.read()
        with open(file2, "r") as fp:
            self.m_Str2 = fp.read()
        self.CompareByStr(self.m_Str1, self.m_Str2)

        # self.m_LCodeWidget
    def CompareByStr(self, str1, str2):
        differ = difflib.Differ()
        diff = differ.compare(self.m_Str1.splitlines(),
                              self.m_Str2.splitlines())
        lstDiff = list(diff)

        lstResult = []
        dInfo = {}
        iLNum = iRight = 1
        bSave = True
        i = 0
        while i < len(lstDiff):
            prefix = lstDiff[i][:2]
            text = lstDiff[i][2:]

            if(bSave and dInfo):
                lstResult.append(copy.deepcopy(dInfo))
                dInfo = {}

            if prefix == "- ":
                dInfo["lNum"] = iLNum
                dInfo["lLine"] = text
                iLNum += 1
                if(i+1 < len(lstDiff) and lstDiff[i+1].startswith("? ")):
                    tmp = lstDiff[i+1][2:]
                    dInfo["ldiff"] = [t.start()
                                      for t in re.finditer("\^", tmp)]
                    i += 1
                    bSave = False

            elif prefix == "+ ":
                dInfo["rNum"] = iRight
                dInfo["rLine"] = text
                iRight += 1
                if(i+1 < len(lstDiff) and lstDiff[i+1].startswith("? ")):
                    tmp = lstDiff[i+1][2:]
                    dInfo["rdiff"] = [t.start()
                                      for t in re.finditer("\^", tmp)]
                    i += 1
                    bSave = True

            elif prefix == "  ":
                dInfo["lNum"] = iLNum
                dInfo["lLine"] = text
                dInfo["rNum"] = iRight
                dInfo["rLine"] = text
                iLNum += 1
                iRight += 1

            i += 1

        lstResult.append(copy.deepcopy(dInfo))
