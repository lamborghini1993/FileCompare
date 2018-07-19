# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-10 15:10:43
@Desc:
"""

import sys
import os
import difflib
import re
import res_rc

from PyQt5 import QtWidgets, QtCore
from . import define, treewidget
from ui import mainwidget_ui
from lib import style


class CMainWidget(QtWidgets.QMainWindow, mainwidget_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(CMainWidget, self).__init__(parent)
        self.setupUi(self)
        self.m_LeftSrc = ""     # 真实的文本，原文
        self.m_RightSrc = ""
        self.m_FilterNormal = ["time"]    # 正常的过滤
        self.m_FilterRE = ["super.*self"]        # 正则过滤
        self.m_CmpResult = {}
        self.InitUI()
        self.InitConnect()
        self.Refersh(define.TEST_FILE1, define.TEST_FILE2)

    def InitUI(self):
        self.setStyleSheet(style.GetSytle())
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 8)
        self.splitter.setStretchFactor(2, 2)

    def InitConnect(self):
        self.plainTextEdit_left.BindBroEditor(self.plainTextEdit_right)
        self.plainTextEdit_right.BindBroEditor(self.plainTextEdit_left)
        self.pushButton_ChooseDir.clicked.connect(self.ChooseDir)

    def ChooseDir(self):
        # sDir = QtWidgets.QFileDialog.getExistingDirectory(self, "选择log文件夹")
        # if not sDir:
        #     return
        sDir = r"E:\mygithub\FileCompare\test"
        iSystemModel = treewidget.CMyFileSystemModel(self)
        index = iSystemModel.setRootPath(sDir)
        self.treeView.header().hide()
        self.treeView.setModel(iSystemModel)
        self.treeView.setRootIndex(index)

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
        diff = differ.compare(self.m_LeftSrc.splitlines(), self.m_RightSrc.splitlines())
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
                dInfo["type"] = define.MODIFICATION.EQUAL
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

            lColor, lAct, rColor, rAct = self.GetFilterResult(dInfo)
            self.plainTextEdit_left.AddLineInfo(iRealNum, dInfo.get("lNum", ""), lColor, lAct)
            self.plainTextEdit_right.AddLineInfo(iRealNum, dInfo.get("rNum", ""), rColor, rAct)

        self.plainTextEdit_left.Load(sLeftContent)
        self.plainTextEdit_right.Load(sRightContent)

    def GetFilterResult(self, dInfo):
        """获取过滤结果"""
        if(dInfo.get("type", "") == define.MODIFICATION.EQUAL):  # 一样
            return define.LINECOLOR.EQUAL, define.LINEACT.NONE, define.LINECOLOR.EQUAL, define.LINEACT.NONE

        sLeft = dInfo.get("lLine", "")
        sRight = dInfo.get("rLine", "")

        bLFilter = self.ValueFilter(sLeft) 
        bRFilter = self.ValueFilter(sRight)
        if(bLFilter or bRFilter):  # 符合过滤，一样
            lColor = rColor = define.LINECOLOR.FILTER
            if not bLFilter:
                lColor = define.LINECOLOR.DEL
            if not bRFilter:
                rColor = define.LINECOLOR.DEL
            return lColor, define.LINEACT.NONE, rColor, define.LINEACT.NONE

        if "lLine" in dInfo and "rLine" not in dInfo:  # 左边添加
            return define.LINECOLOR.ADD, define.LINEACT.LEFTADD, define.LINECOLOR.DEL, define.LINEACT.NONE

        if "lLine" not in dInfo and "rLine" in dInfo:  # 右边添加
            return define.LINECOLOR.DEL, define.LINEACT.NONE, define.LINECOLOR.ADD, define.LINEACT.RIGHTADD
        # 不一样
        return define.LINECOLOR.LMODIFY, define.LINEACT.MODIFY, define.LINECOLOR.RMODIFY, define.LINEACT.MODIFY

    def ValueFilter(self, sInfo):
        """判断是否需要过滤"""
        if not sInfo:
            return False
        for line in self.m_FilterNormal:
            if sInfo.find(line) != -1:
                return True
        for line in self.m_FilterRE:
            if re.search(line, sInfo):
                return True
        return False


def Show():
    app = QtWidgets.QApplication(sys.argv)
    obj = CMainWidget()
    obj.show()
    sys.exit(app.exec_())
