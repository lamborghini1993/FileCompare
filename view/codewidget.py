# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-19 14:02:33
@Desc: 代码对比的控件
"""

import weakref
import time
import os
import re
import hashlib
import define

from PyQt5 import QtWidgets, QtCore, QtGui

FRAME_RE = r"@framestart.*?@frameend"
CUR_FRAME = r"!#curframe:(\d+)"
MAX_NUM = 99999999


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
            y = fSingleH * iBlock + self.width()
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
    CLEAR_PLAIN_TEXT_EDIT = QtCore.pyqtSignal()

    def __init__(self, *args):
        super(CCodeEdit, self).__init__(*args)
        self.m_BindEditor = None
        self.m_BindLabel = None
        self.m_MinFrame = MAX_NUM
        self.m_MaxFrame = 0
        self.m_LineNumArea = CLineNumArea(self)
        self.m_ScrollBar = CScrollBar(self)
        self.Init()
        self.InitUI()
        self.InitConnect()

    def Init(self):
        self.m_LineInfo = {}        # 真实行号:(原来行号,行首变化行为)  下标从0开始
        self.m_BlockBgInfo = {}     # 真实行号:每行的颜色   下标从0开始
        self.m_ModBlockList = []    # 存放修改的块
        self.m_LastModLine = -1
        self.m_bDragIn = False
        self.m_CurFile = None

    def InitUI(self):
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setVerticalScrollBar(self.m_ScrollBar)
        self.setTabStopWidth(self.fontMetrics().width("_") * 4)
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setReadOnly(True)
        self.E_UpdateLineNumAreaWidth(0)
        self.SetShowTabAndSpaces(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setAcceptDrops(True)

    def InitConnect(self):
        self.blockCountChanged.connect(self.E_UpdateLineNumAreaWidth)
        self.updateRequest.connect(self.E_UpdateLineNumArea)
        self.cursorPositionChanged.connect(self.E_ChangedCursor)
        self.cursorPositionChanged.connect(self.E_UpdateSelBlock)

    def resizeEvent(self, re):
        super(CCodeEdit, self).resizeEvent(re)
        qRect = self.contentsRect()
        cr1 = QtCore.QRect(qRect.left(), qRect.top(), self.LineNumAreaWidth(), qRect.height())
        self.m_LineNumArea.setGeometry(cr1)

    def BindBroEditor(self, oEditor):
        if self.m_BindEditor:
            return
        self.m_BindEditor = weakref.ref(oEditor)
        self.verticalScrollBar().valueChanged.connect(self.OnVScrollBarValChanged)
        self.horizontalScrollBar().valueChanged.connect(self.OnHScrollBarValChanged)

    def BindLabel(self, oLabel):
        self.m_BindLabel = weakref.ref(oLabel)

    def OnVScrollBarValChanged(self, iVal):
        self.m_BindEditor().verticalScrollBar().setValue(iVal)

    def OnHScrollBarValChanged(self, iVal):
        self.m_BindEditor().horizontalScrollBar().setValue(iVal)

    def AddLineInfo(self, realNum, showNum, lineColor, lineAct):
        showNum = str(showNum)
        self.m_LineInfo[realNum] = (showNum, lineAct.value)
        self.m_BlockBgInfo[realNum] = lineColor.value

    def AddModBlock(self, realNum):
        if(realNum != self.m_LastModLine + 1):
            self.m_ModBlockList.append(realNum)
        self.m_LastModLine = realNum

    def Load(self, text):
        self.setPlainText(text)
        self.ProcessBlkBg()
        self.m_ScrollBar.SetBlockBgInfo(self.m_BlockBgInfo)

    def ProcessBlkBg(self):
        """设置每个行块的背景"""
        doc = self.document()
        oCursor = QtGui.QTextCursor(doc)
        for iLine, bgColor in self.m_BlockBgInfo.items():
            blk = doc.findBlockByLineNumber(iLine)
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

    def E_UpdateLineNumAreaWidth(self, _):
        self.setViewportMargins(self.LineNumAreaWidth() + 20, 0, 0, 0)

    def E_UpdateLineNumArea(self, qRect, iDy):
        if iDy:
            self.m_LineNumArea.scroll(0, iDy)
        else:
            self.m_LineNumArea.update(0, qRect.y(), self.m_LineNumArea.width(), qRect.height())
        if qRect.contains(self.viewport().rect()):
            self.E_UpdateLineNumAreaWidth(0)

    def E_ChangedCursor(self):
        oTxtCursor = self.textCursor()
        sCurWord = str(oTxtCursor.selectedText())
        if sCurWord:
            self._HightLightSelectWord(sCurWord)
            self.m_BindEditor()._HightLightSelectWord(sCurWord)
        else:
            self._HightLightSelectLine()
            self.m_BindEditor()._HightLightSelectLine()
        # TODO:scrollbar颜色跟着改变

    def _HightLightSelectLine(self):
        """高亮选择的行"""
        extSelections = []
        lineSelection = QtWidgets.QTextEdit.ExtraSelection()
        lineColor = QtGui.QColor(QtCore.Qt.green).lighter(160)
        lineSelection.format.setBackground(lineColor)
        lineSelection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        lineSelection.cursor = self.textCursor()
        extSelections.append(lineSelection)
        self.setExtraSelections(extSelections)

    def _HightLightSelectWord(self, sCurWord):
        """高亮选择的单词"""
        extSelections = []
        lstCurWordCursor = []
        iFindOpt = QtGui.QTextDocument.FindCaseSensitively | QtGui.QTextDocument.FindWholeWords
        oTargetCursor = self.document().find(sCurWord, 0, iFindOpt)
        while not oTargetCursor.isNull():
            lstCurWordCursor.append(oTargetCursor)
            oTargetCursor = self.document().find(sCurWord, oTargetCursor, iFindOpt)
        for oCursor in lstCurWordCursor:
            wordSelection = QtWidgets.QTextEdit.ExtraSelection()
            wordSelection.format.setBackground(define.LINECOLOR.WORDSELECT.value)
            wordSelection.cursor = oCursor
            extSelections.append(wordSelection)
        self.setExtraSelections(extSelections)

    def E_UpdateSelBlock(self):
        iBlock = self.textCursor().blockNumber()
        self.m_BindEditor().MoveCursorToBlock(iBlock)

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
                sTextNum, sPngAct = self.m_LineInfo.get(iBlockNum, (iBlockNum, None))
                qPainter.setPen(QtCore.Qt.black)
                qPainter.drawText(0, iTop, iDrawWidth, iFontHeight, QtCore.Qt.AlignCenter, str(sTextNum))
                if sPngAct:
                    oPngAct = GetLinePixMap(sPngAct)
                    oPngAct = oPngAct.scaled(iFontHeight, iFontHeight)
                    qPainter.drawPixmap(iDrawWidth, iTop, iFontHeight, iFontHeight, oPngAct)
            qBlock = qBlock.next()
            iTop = iBottom
            iBottom = iTop + int(self.blockBoundingRect(qBlock).height())
            iBlockNum += 1

    def CanDrag(self, event):
        """判断是否支持拖拽"""
        return True
        # if not event.mimeData().hasText():
        #     return False
        # data = str(event.mimeData().text())
        # if data.startswith("open "):
        #     return True
        # return False

    def dragEnterEvent(self, event):
        """拖动操作进入本窗口"""
        super(CCodeEdit, self).dragEnterEvent(event)
        if not self.CanDrag(event):
            event.ignore()
            return
        event.accept()
        event.acceptProposedAction()
        self.m_bDragIn = True

    def dragLeaveEvent(self, event):
        """拖动离开触发"""
        super(CCodeEdit, self).dragLeaveEvent(event)
        self.m_bDragIn = False

    def dragMoveEvent(self, event):
        if not self.CanDrag(event):
            event.ignore()
            return
        event.accept()
        event.acceptProposedAction()

    def dropEvent(self, event):
        """放开了鼠标完成drop操作"""
        super(CCodeEdit, self).dropEvent(event)
        if not self.CanDrag(event):
            event.ignore()
            return
        self.m_bDragIn = False
        event.acceptProposedAction()
        self.m_CurFile = str(event.mimeData().text())
        if(self.m_CurFile.startswith("file:///")):
            self.m_CurFile = self.m_CurFile[8:]
        self.m_MaxFrame = 0
        self.m_MinFrame = MAX_NUM
        self.SplitFileByFrame()
        self.CLEAR_PLAIN_TEXT_EDIT.emit()

    def SplitFileByFrame(self):
        hashFile = hashlib.md5(self.m_CurFile.encode("utf-8")).hexdigest()
        with open(self.m_CurFile, "r", encoding="utf-8") as fp:
            lines = fp.read()
            lstFrame = re.findall(FRAME_RE, lines, flags=re.DOTALL)
            for frams in lstFrame:
                oMatch = re.search(CUR_FRAME, frams, flags=re.DOTALL)
                if not oMatch:
                    continue
                num = oMatch.group()[11:]
                newfile = os.path.join(define.CACHE_DIR, hashFile + "_" + num)
                self.m_MinFrame = min(int(num), self.m_MinFrame)
                self.m_MaxFrame = max(int(num), self.m_MaxFrame)
                if(os.path.exists(newfile)):
                    continue
                with open(newfile, "w", encoding="utf-8") as ffp:
                    ffp.write(frams)
        labelText = os.path.basename(self.m_CurFile) + "(%s-%s)" % (self.m_MinFrame, self.m_MaxFrame)
        self.m_BindLabel().setText(labelText)

    def JumpToPreviousMod(self):
        """跳转到上一个修改的地方"""
        self.JumpToMod(False)

    def JumpToNextMod(self):
        """跳转到上一个修改的地方"""
        self.JumpToMod(True)

    def JumpToMod(self, bNext=True):
        iCurBlock = self.textCursor().blockNumber()
        iNextIndex = self.BinarySearch(iCurBlock)
        if not bNext:   # 向上
            if iCurBlock in self.m_ModBlockList:
                iNextIndex -= 2
            else:
                iNextIndex -= 1
        iNextIndex = (iNextIndex + len(self.m_ModBlockList)) % len(self.m_ModBlockList)
        iNextBlock = self.m_ModBlockList[iNextIndex]
        self.MoveCursorToBlock(iNextBlock)
        self.centerCursor()
        self.m_BindEditor().centerCursor()

    def BinarySearch(self, iBlock):
        """列表中用二分查找一个大于iBlock的下标"""
        l = 0
        r = len(self.m_ModBlockList)
        while l <= r:
            m = (l + r) // 2
            v = self.m_ModBlockList[m]
            if (iBlock > v):
                l = m + 1
            elif (iBlock < v):
                r = m - 1
            else:
                return m + 1
        return l

    def MoveCursorToBlock(self, iBlock):
        tc = self.textCursor()
        iCurBlock = tc.blockNumber()
        iOffset = abs(iCurBlock - iBlock)
        if iCurBlock > iBlock:
            tc.movePosition(QtGui.QTextCursor.Up, n=iOffset)
        else:
            tc.movePosition(QtGui.QTextCursor.Down, n=iOffset)
        self.setTextCursor(tc)
