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
import define
import hashlib

from PyQt5 import QtWidgets, QtCore
from . import treewidget
from ui import mainwidget_ui
from lib import style, misc


class CMainWidget(QtWidgets.QMainWindow, mainwidget_ui.Ui_MainWindow):
    m_JsonFile = "config.json"

    def __init__(self, parent=None):
        super(CMainWidget, self).__init__(parent)
        self.setupUi(self)
        self.m_LeftSrc = []     # 真实的文本，原文
        self.m_RightSrc = []
        self.m_FilterInfo = {}        # 方案：正则过滤列表
        self.m_CmpResult = {}
        self.InitUI()
        self.InitBind()
        self.InitConnect()
        self.Load()

    def InitUI(self):
        self.setStyleSheet(style.GetSytle())
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 8)
        self.splitter.setStretchFactor(2, 2)

    def InitBind(self):
        self.plainTextEdit_left.BindBroEditor(self.plainTextEdit_right)
        self.plainTextEdit_right.BindBroEditor(self.plainTextEdit_left)
        self.plainTextEdit_left.BindLabel(self.label_left)
        self.plainTextEdit_right.BindLabel(self.label_right)

    def InitConnect(self):
        self.pushButton_ChooseDir.clicked.connect(self.E_ChooseDir)
        self.pushButton_compare.clicked.connect(self.E_Compare)
        self.comboBox.currentTextChanged.connect(self._LoadFilterTextEdit)
        self.comboBox.editTextChanged.connect(self._LoadFilterTextEdit)
        self.plainTextEdit_left.CLEAR_PLAIN_TEXT_EDIT.connect(self.E_ClearPlainTextEdit)
        self.plainTextEdit_right.CLEAR_PLAIN_TEXT_EDIT.connect(self.E_ClearPlainTextEdit)
        self.pushButton_Down.clicked.connect(self.plainTextEdit_left.JumpToNextMod)
        self.pushButton_Up.clicked.connect(self.plainTextEdit_left.JumpToPreviousMod)
        self.pushButton_Find.clicked.connect(self.plainTextEdit_left.m_FindWidget.Open)

    def Load(self):
        self.m_Info = misc.JsonLoad(self.m_JsonFile, {})
        self.m_FilterInfo = self.m_Info.setdefault("filterInfo", {})
        self.m_OpenDir = self.m_Info.setdefault("dir", "")
        if self.m_OpenDir:
            self._LoadDirTree()
        if self.m_FilterInfo:
            lstFilter = list(self.m_FilterInfo.keys())
            fangan = lstFilter[0]
            self.comboBox.addItems(lstFilter)
            self.comboBox.setCurrentText(fangan)

    def _LoadFilterTextEdit(self, fangan):
        """加载过滤方案"""
        lstRE = self.m_FilterInfo.get(fangan, [])
        textEdit = "\n".join(lstRE)
        self.comboBox.setCurrentText(fangan)
        self.textEdit.setText(textEdit)

    def _LoadDirTree(self):
        oSystemModel = treewidget.CMyFileSystemModel(self)
        index = oSystemModel.setRootPath(self.m_OpenDir)
        self.treeView.SetFileSystemModel(oSystemModel)
        self.treeView.header().hide()
        self.treeView.setModel(oSystemModel)
        self.treeView.setRootIndex(index)

    def Save(self):
        self.m_Info["dir"] = self.m_OpenDir
        misc.JsonDump(self.m_Info, self.m_JsonFile)

    def E_ChooseDir(self):
        self.m_OpenDir = QtWidgets.QFileDialog.getExistingDirectory(self, "选择log文件夹")
        if self.m_OpenDir:
            self._LoadDirTree()
            self.Save()

    def E_Compare(self):
        fangan = self.comboBox.currentText()
        lstRe = self.textEdit.toPlainText().splitlines()
        if fangan not in self.m_FilterInfo:
            self.comboBox.addItem(fangan)
        self.m_FilterInfo[fangan] = [line for line in lstRe if line]
        self.Save()
        if(self._ValidTwoPlain()):
            self._StartCompare()

    def _StartCompare(self):
        start = int(self.spinBox_start.text())
        end = int(self.spinBox_end.text())
        self.m_LeftSrc = self._GetFileList(self.plainTextEdit_left.m_CurFile, start, end)
        self.m_RightSrc = self._GetFileList(self.plainTextEdit_right.m_CurFile, start, end)
        self.m_CmpResult = {}
        self.plainTextEdit_left.Init()
        self.plainTextEdit_right.Init()
        self.CompareByStr()
        self.RefershCmp()
        self.pushButton_Down.click()  # 选择第一个不同的行

    def _GetFileList(self, files, start, end):
        lst = []
        hashFile = hashlib.md5(files.encode("utf-8")).hexdigest()
        hashFile = os.path.join(define.CACHE_DIR, hashFile)
        for x in range(start, end+1):
            fileTmp = hashFile + "_" + str(x)
            if not os.path.exists(fileTmp):
                continue
            with open(fileTmp, "r", encoding="utf-8") as fp:
                lstTmp = fp.read().splitlines()
                lst += lstTmp
        return lst

    def _ValidTwoPlain(self):
        if(self.plainTextEdit_left.m_CurFile and self.plainTextEdit_right.m_CurFile):
            return True
        return False

    def E_ClearPlainTextEdit(self):
        self.plainTextEdit_left.clear()
        self.plainTextEdit_right.clear()
        if(self._ValidTwoPlain()):
            maxLeft = max(self.plainTextEdit_left.m_MinFrame, self.plainTextEdit_right.m_MinFrame)
            minRight = min(self.plainTextEdit_left.m_MaxFrame, self.plainTextEdit_right.m_MaxFrame)
            if(maxLeft <= minRight):    # 有帧的交集
                self.label_Frame.setText("%s-%s帧" % (maxLeft, minRight))
                self.spinBox_start.setMinimum(maxLeft)
                self.spinBox_start.setMaximum(minRight)
                self.spinBox_end.setMinimum(maxLeft)
                self.spinBox_end.setMaximum(minRight)
            else:   # 无帧的交集
                self.label_Frame.setText("无共同帧")

    def CompareByStr(self):
        differ = difflib.Differ()
        diff = differ.compare(self.m_LeftSrc, self.m_RightSrc)
        lstDiff = list(diff)
        dResult = self.m_CmpResult
        iLNum = iRight = 1  # 原来文本文件的行数
        iLRealNum = iRRealNum = 0   # 真实的QPlainTextEditor的行数，因为控件是从0开始的，所以初始化为0
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
            if self._IsModify(lAct) or self._IsModify(rAct):
                self.plainTextEdit_left.AddModBlock(iRealNum)
                self.plainTextEdit_right.AddModBlock(iRealNum)
            self.plainTextEdit_left.AddLineInfo(iRealNum, dInfo.get("lNum", ""), lColor, lAct)
            self.plainTextEdit_right.AddLineInfo(iRealNum, dInfo.get("rNum", ""), rColor, rAct)
            self.plainTextEdit_left.AddSpaceNum(iRealNum, self._FindSpaceNum(sLeft))
            self.plainTextEdit_right.AddSpaceNum(iRealNum, self._FindSpaceNum(sRight))

        self.plainTextEdit_left.Load(sLeftContent)
        self.plainTextEdit_right.Load(sRightContent)

    def _FindSpaceNum(self, line):
        """查找有几个空格，折叠使用"""
        iNum = 0
        for char in line:
            if ord(char) == 32:  # 空格
                iNum += 1
            else:
                return iNum
        return -1   # 全都是空格

    def _IsModify(self, act):
        if act in (define.LINEACT.LEFTADD, define.LINEACT.RIGHTADD, define.LINEACT.MODIFY):
            return True
        return False

    def GetFilterResult(self, dInfo):
        """获取过滤结果"""
        if(dInfo.get("type", "") == define.MODIFICATION.EQUAL):  # 一样
            return define.LINECOLOR.EQUAL, define.LINEACT.NONE, define.LINECOLOR.EQUAL, define.LINEACT.NONE

        sLeft = dInfo.get("lLine", "")
        sRight = dInfo.get("rLine", "")

        bLFilter = self.ValueFilter(sLeft)
        bRFilter = self.ValueFilter(sRight)
        if(bLFilter or bRFilter):  # 符合过滤，一样
            left = right = define.LINECOLOR.FILTER, define.LINEACT.FILTER
            if not bLFilter:
                left = define.LINECOLOR.DEL, define.LINEACT.NONE
            if not bRFilter:
                right = define.LINECOLOR.DEL, define.LINEACT.NONE
            return left[0], left[1], right[0], right[1]

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
        fangan = self.comboBox.currentText()
        for line in self.m_FilterInfo.get(fangan, ""):
            if re.search(line, sInfo):
                return True
        return False


def Show():
    app = QtWidgets.QApplication(sys.argv)
    obj = CMainWidget()
    obj.show()
    sys.exit(app.exec_())
