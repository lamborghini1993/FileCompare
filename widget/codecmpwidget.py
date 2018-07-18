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
import time

from PyQt5 import QtWidgets, QtCore, QtGui

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
    LEFTADD = "minus"
    RIGHTADD = "plus"
    MODIFY = "modify"
    NONE = None


def GetLinePixMap(png):
    if png:
        bgPix = QtGui.QPixmap(":/app/%s.png" % png)
    else:
        bgPix = None
    return bgPix


class CScrollBar(QtWidgets.QScrollBar):
    """可以指定显示文本位置的纵向滚动条"""

    m_MinBlockHeight = 8

    def __init__(self, parent):
        # super(CScrollBar, self).__init__(parent)
        super(CScrollBar, self).__init__(QtCore.Qt.Vertical, parent)
        self.m_BlockBgDict = {}
        self.m_Parent = weakref.ref(parent)

    def SetBlockBgInfo(self, dBlkBgInfo):
        self.m_BlockBgDict = dBlkBgInfo
        self.update()

    def paintEvent(self, pe):
        """绘画事件"""
        super(CScrollBar, self).paintEvent(pe)
        painter = QtGui.QPainter(self)
        parent = self.m_Parent()
        dh = parent.blockCount()
        sh = self.height() - self.width() * 2
        fSingleH = sh / dh
        fBlkHeight = max(self.m_MinBlockHeight, fSingleH)
        w = self.width() - 8
        for iBlock, bgColor in self.m_BlockBgDict.items():
            x = 4
            y = fSingleH * (iBlock - 1) + self.width()
            rect = QtCore.QRectF(x, y, w, fBlkHeight)
            painter.fillRect(rect, bgColor)


class CLineNumArea(QtWidgets.QWidget):
    def __init__(self, parent):
        super(CLineNumArea, self).__init__(parent)
        self.m_Parent = weakref.ref(parent)

    def sizeHint(self):
        super(CLineNumArea, self).sizeHint()
        qSize = QtCore.QSize(self.m_Parent().LineNumAreaWidth(), 0)
        return qSize

    def paintEvent(self, pe):
        super(CLineNumArea, self).paintEvent(pe)
        self.m_Parent().LineNumAreaPaintEvent(pe)


class CCodeEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, *args):
        super(CCodeEdit, self).__init__(*args)
        self.m_BindEditor = None
        self.m_LineNum = 0      # 代码的行数
        self.m_LineInfo = {}    # 真实行号:(原来行号,行首变化行为)
        self.m_BlockBgInfo = {}  # 真实行号:每行的颜色
        self.m_LineNumArea = CLineNumArea(self)
        self.m_ScrollBar = CScrollBar(self)
        self.setVerticalScrollBar(self.m_ScrollBar)

        # 设置字体
        oFont = QtGui.QFont()
        oFont.setFamily("Consolas")
        self.setFont(oFont)

        self.setTabStopWidth(self.fontMetrics().width("_") * 4)
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setReadOnly(True)
        self.UpdateLineNumAreaWidth(0)
        self.SetShowTabAndSpaces(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def resizeEvent(self, re):
        super(CCodeEdit, self).resizeEvent(re)
        qRect = self.contentsRect()
        cr1 = QtCore.QRect(qRect.left(), qRect.top(), self.LineNumAreaWidth(), qRect.height())
        self.m_LineNumArea.setGeometry(cr1)

    def BindBroEditor(self, oEditor):
        if self.m_BindEditor:
            return
        self.m_BindEditor = weakref.ref(oEditor)
        # TODO

    def AddLineInfo(self, realNum, showNum, lineColor, lineAct):
        showNum = str(showNum)
        self.m_LineInfo[realNum] = (showNum, lineAct.value)
        self.m_BlockBgInfo[realNum] = lineColor.value

    def Load(self, text):
        self.setPlainText(text)
        self.ProcessBlkBg()
        self.m_ScrollBar.SetBlockBgInfo(self.m_BlockBgInfo)

    def ProcessBlkBg(self):
        """设置每个行块的背景"""
        doc = self.document()
        oCursor = QtGui.QTextCursor(doc)
        for iLine, bgColor in self.m_BlockBgInfo.items():
            blk = doc.findBlockByLineNumber(iLine - 1)  # 下标从0开始
            oCursor.setPosition(blk.position())
            oCursor.beginEditBlock()
            oCursor.select(QtGui.QTextCursor.LineUnderCursor)
            fmt = QtGui.QTextBlockFormat()
            fmt.setBackground(bgColor)
            oCursor.mergeBlockFormat(fmt)
            oCursor.clearSelection()
            oCursor.endEditBlock()

    def SetShowTabAndSpaces(self, bShow):
        doc = self.document()
        op = doc.defaultTextOption()
        if bShow:
            op.setFlags(op.flags() | QtGui.QTextOption.ShowTabsAndSpaces)
        else:
            op.setFlags(op.flags() | ~QtGui.QTextOption.ShowTabsAndSpaces)
            op.setFlags(op.flags() | QtGui.QTextOption.AddSpaceForLineAndParagraphSeparators)
        doc.setDefaultTextOption(op)

    def UpdateLineNumAreaWidth(self):
        self.setViewportMargins(self.LineNumAreaWidth() + 20, 0, 0, 0)

    def LineNumAreaWidth(self):
        """获取宽度"""
        iDigits = 0
        iMax = max(1, self.blockCount())
        while iMax:
            iMax //= 10
            iDigits += 1
        iWidth = self.fontMetrics().width("9") * (iDigits + 3)
        return iWidth

    def LineNumAreaPaintEvent(self, pe):
        """更新行号的显示，处理空白行号"""
        qPainter = QtGui.QPainter(self.m_LineNumArea)
        qPainter.fillRect(pe.rect(), QtCore.Qt.darkGray)
        qBlock = self.firstVisibleBlock()
        iBlockNum = qBlock.blockNumber()
        qRectF = self.blockBoundingGeometry(qBlock)
        iTop = int(qRectF.translated(self.contentOffset()).top())
        iBottom = iTop + int(qRectF.height())
        iFontHeight = self.fontMetrics().height()
        iFontWidth = self.fontMetrics().width("9")
        iDrawWidth = self.m_LineNumArea.width() - iFontWidth * 3
        while(qBlock.isValid() and iTop <= pe.rect().bottom()):
            if qBlock.isVisible() and iBottom >= pe.rect().top():
                sNum = str(iBlockNum + 1)   # 真实的行号
                sTextNum, sPngAct = self.m_LineInfo.get(iBlockNum + 1, (sNum, None))
                qPainter.setPen(QtCore.Qt.black)
                qPainter.drawText(0, iTop, iDrawWidth, iFontHeight, QtCore.Qt.AlignCenter, sTextNum)
                if sPngAct:
                    oPngAct = GetLinePixMap(sPngAct)
                    oPngAct = oPngAct.scaled(iFontHeight, iFontHeight)
                    qPainter.drawPixmap(iDrawWidth, iTop, iFontHeight, iFontHeight, oPngAct)
            qBlock = qBlock.next()
            iTop = iBottom
            iBottom = iTop + int(self.blockBoundingRect(qBlock).height())
            iBlockNum += 1


class CCodeCmpWidget(QtWidgets.QWidget):
    def __init__(self, *args):
        super(CCodeCmpWidget, self).__init__(*args)
        self.m_LeftSrc = ""     # 真实的文本，原文
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

            if "ldiff" in dInfo:    # 不一样-小范围个别单词修改
                self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.LMODIFY, LINEACT.MODIFY)
                self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.RMODIFY, LINEACT.MODIFY)

            elif "lLine" in dInfo and "rLine" not in dInfo:  # 左边添加
                self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.ADD, LINEACT.LEFTADD)
                self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.DEL, LINEACT.NONE)

            elif "lLine" not in dInfo and "rLine" in dInfo:  # 右边添加
                self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.DEL, LINEACT.NONE)
                self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.ADD, LINEACT.RIGHTADD)

            else:   # 一样
                if(dInfo.get("type", "") == MODIFICATION.EQUAL):
                    self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.EQUAL, LINEACT.NONE)
                    self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.EQUAL, LINEACT.NONE)
                else:   # 不一样-整行修改
                    self.m_LCodeWidget.AddLineInfo(iRealNum, dInfo.get("lNum", ""), LINECOLOR.LMODIFY, LINEACT.MODIFY)
                    self.m_RCodeWidget.AddLineInfo(iRealNum, dInfo.get("rNum", ""), LINECOLOR.RMODIFY, LINEACT.MODIFY)

        self.m_LCodeWidget.Load(sLeftContent)
        self.m_RCodeWidget.Load(sRightContent)
