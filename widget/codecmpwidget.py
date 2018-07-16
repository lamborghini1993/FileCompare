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
import enum

from PyQt5 import QtWidgets, QtCore, QtGui
from . import codewidget

file1 = r"E:\mygithub\FileCompare\test\py2ui.py"
file2 = r"E:\mygithub\FileCompare\test\py2ui2.py"


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
    # ADD = QtGui.QPixmap(":/app/plus.png")
    # DEL = QtGui.QPixmap(":/app/minus.png")
    # MODIFY = QtGui.QPixmap(":/app/modify.png")
    ADD = "plus"
    DEL = "minus"
    MODIFY = "modify"
    NONE = None


class CCodeEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, *args):
        super(CCodeEdit, self).__init__(*args)
        self.m_BindEditor = None
        self.m_LineInfo = {}    # 真实行号:(原来行号,每行的颜色,行首变化行为)

    def BindBroEditor(self, oEditor):
        if self.m_BindEditor:
            return
        self.m_BindEditor = weakref.ref(oEditor)
        # TODO

    def AddLineInfo(self, realNum, showNum, lineColor, lineAct):
        showNum = str(showNum)
        self.m_LineInfo[realNum] = (showNum, lineColor, lineAct)

    def Load(self, text):
        self.setPlainText(text)


class CCodeCmpWidget(QtWidgets.QWidget):
    def __init__(self, *args):
        super(CCodeCmpWidget, self).__init__(*args)
        self.m_LeftSrc = ""     # 真实的文本，原文
        self.m_RightSrc = ""
        # self.m_LShowSrc = ""    # 左边显示的文本
        # self.m_RShowSrc = ""
        self.m_CmpResult = {}
        self.m_HLayout = QtWidgets.QHBoxLayout(self)
        self.m_LCodeWidget = CCodeEdit()
        self.m_RCodeWidget = CCodeEdit()

        self.m_Splitter = QtWidgets.QSplitter(self)
        self.m_Splitter.addWidget(self.m_LCodeWidget)
        self.m_Splitter.addWidget(self.m_RCodeWidget)
        self.m_HLayout.addWidget(self.m_Splitter)
        self.show()
        self.Refersh(file1, file2)

    def Refersh(self, leftFile, rightFile):
        with open(leftFile, "r", encoding="utf8") as fp:
            self.m_LeftSrc = fp.read()
        with open(rightFile, "r", encoding="utf8") as fp:
            self.m_RightSrc = fp.read()
        self.m_CmpResult = {}
        self.CompareByStr()
        self.RefershCmp()

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
                if(i + 1 < len(lstDiff) and lstDiff[i + 1].startswith("? ")):
                    iLRealNum = iRRealNum = max(iLRealNum, iRRealNum)
                    dInfo = dResult.setdefault(iLRealNum, {})
                    tmp = lstDiff[i + 1][2:]
                    dInfo["ldiff"] = [t.start() for t in re.finditer("\^", tmp)]
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
                if(i + 1 < len(lstDiff) and lstDiff[i + 1].startswith("? ")):
                    tmp = lstDiff[i + 1][2:]
                    dInfo["rdiff"] = [t.start() for t in re.finditer("\^", tmp)]
                    i += 1

            elif prefix == "  ":
                iLRealNum = iRRealNum = max(iLRealNum, iRRealNum)
                dInfo = dResult.setdefault(iRRealNum, {})
                dInfo["lNum"] = iLNum
                dInfo["lLine"] = text
                dInfo["rNum"] = iRight
                dInfo["rLine"] = text
                dInfo["type"] = MODIFICATION.EQUAL
                iLRealNum += 1
                iRRealNum += 1
                iLNum += 1
                iRight += 1

            i += 1

    def RefershCmp(self):
        sLeftContent = sRightContent = ""
        for iRealNum, dInfo in self.m_CmpResult.items():
            sLeft = dInfo.get("lLine", "")
            sRight = dInfo.get("rLine", "")
            if sLeftContent:
                sLeftContent += "\n" + sLeft
            else:
                sLeftContent = sLeft

            if sRightContent:
                sRightContent += "\n" + sRight
            else:
                sRightContent = sRight

            if "ldiff" in dInfo:    # 修改
                self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.LMODIFY, LINEACT.MODIFY)
                self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.RMODIFY, LINEACT.MODIFY)

            elif "lLine" in dInfo and "rLine" not in dInfo:  # 左边添加
                self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.ADD, LINEACT.ADD)
                self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.DEL, LINEACT.DEL)

            elif "lLine" not in dInfo and "rLine" in dInfo:  # 右边添加
                self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.ADD, LINEACT.DEL)
                self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.DEL, LINEACT.ADD)

            else:   # 一样
                self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.EQUAL, LINEACT.NONE)
                self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.EQUAL, LINEACT.NONE)

        self.m_LCodeWidget.Load(sLeftContent)
        self.m_RCodeWidget.Load(sRightContent)
