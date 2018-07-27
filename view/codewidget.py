# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-19 14:02:33
@Desc: 代码对比的控件
"""

import weakref
import time
import os
import define

from PyQt5 import QtWidgets, QtCore, QtGui
from . import findwidget
from lib import misc


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

    def mousePressEvent(self, event):
        self.m_Parent().LineAreaPress(event.pos())


class CCodeEdit(QtWidgets.QPlainTextEdit):
    CLEAR_PLAIN_TEXT_EDIT = QtCore.pyqtSignal()

    def __init__(self, *args):
        super(CCodeEdit, self).__init__(*args)
        self.m_BindEditor = None
        self.m_BindLabel = None
        self.m_LineNumArea = CLineNumArea(self)
        self.m_ScrollBar = CScrollBar(self)
        self.m_FindWidget = findwidget.CFindWidget(self)
        self.m_CurFile = None
        self.m_Stack = misc.CStack()
        self.Init()
        self.InitUI()
        self.InitConnect()

    def Init(self):
        self.m_LineNum = 0          # 代码的行数
        self.m_LineInfo = {}        # 真实行号:(原来行号,行首变化行为)  下标从0开始
        self.m_BlockBgInfo = {}     # 真实行号:每行的颜色   下标从0开始
        self.m_ModBlockList = []    # 存放修改的块
        self.m_LastModLine = -1
        self.m_HasLoad = None
        self.m_Stack.clear()
        self.m_FoldStatus = {}  # 真实行:折叠图标
        self.m_FoldBlock = {}   # A行:B行 A行到B行是一个块
        self.m_SpaceNum = {}    # A行:空格数量

    def InitUI(self):
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

    # ------------------begin:重写的方法------------------
    def resizeEvent(self, re):
        super(CCodeEdit, self).resizeEvent(re)
        qRect = self.contentsRect()
        cr1 = QtCore.QRect(qRect.left(), qRect.top(), self.LineNumAreaWidth(), qRect.height())
        self.m_LineNumArea.setGeometry(cr1)
        self.FindWidgetMoveRight()

    def keyPressEvent(self, event):
        if(event.modifiers() == QtCore.Qt.ControlModifier):
            if(event.key() in (QtCore.Qt.Key_Up, QtCore.Qt.Key_E)):
                self.JumpToPreviousMod()
            if(event.key() in (QtCore.Qt.Key_Down, QtCore.Qt.Key_D)):
                self.JumpToNextMod()
            if(event.key() == QtCore.Qt.Key_F):
                self.m_FindWidget.Open()
        if(event.key() == QtCore.Qt.Key_Escape):
            self.m_FindWidget.hide()
        self.m_FindWidget.keyPressEvent(event)

    def dragEnterEvent(self, event):
        """拖动操作进入本窗口"""
        super(CCodeEdit, self).dragEnterEvent(event)
        if not self.CanDrag(event):
            event.ignore()
            return
        event.accept()
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """拖拽移动中"""
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
        event.acceptProposedAction()
        self.m_CurFile = str(event.mimeData().text())
        if(self.m_CurFile.startswith("file:///")):
            self.m_CurFile = self.m_CurFile[8:]
        if(not os.path.exists(self.m_CurFile)):
            self.m_CurFile = ""
            return
        self.m_BindLabel().setText(os.path.basename(self.m_CurFile))
        self.CLEAR_PLAIN_TEXT_EDIT.emit()

    def scrollContentsBy(self, dx, dy):
        self.viewport().update()
        super(CCodeEdit, self).scrollContentsBy(dx, dy)
    # ------------------end:重写的方法------------------

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

    def AddLineInfo(self, iLineNum, showNum, lineColor, lineAct):
        showNum = str(showNum)
        self.m_LineInfo[iLineNum] = (showNum, lineAct.value)
        self.m_BlockBgInfo[iLineNum] = lineColor.value

    def AddModBlock(self, iLineNum):
        if(iLineNum != self.m_LastModLine + 1):
            self.m_ModBlockList.append(iLineNum)
        self.m_LastModLine = iLineNum

    def AddSpaceNum(self, iLineNum, iSpaceNum):
        """添加真实行对应空格个数，折叠使用"""
        self.m_SpaceNum[iLineNum] = iSpaceNum

    def Load(self, text):
        self.m_HasLoad = True
        self.setPlainText(text)
        self.ProcessBlkBg()
        self.m_ScrollBar.SetBlockBgInfo(self.m_BlockBgInfo)
        self._CalculationFold()

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
        self.setViewportMargins(self.LineNumAreaWidth() + 2, 0, 0, 0)

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
        """获取左边栏的宽度"""
        iDigits = 0
        iMax = max(1, self.blockCount())
        while iMax:
            iMax //= 10
            iDigits += 1
        # 数字宽度 + 两张图片的宽度
        iWidth = self.fontMetrics().width("9") * iDigits + self.fontMetrics().height() * 2
        return iWidth

    def LineNumAreaPaintEvent(self, pe):
        """更新行号的显示，处理空白行号"""
        if not self.m_HasLoad:
            return
        qPainter = QtGui.QPainter(self.m_LineNumArea)
        qPainter.fillRect(pe.rect(), QtCore.Qt.darkGray)
        qBlock = self.firstVisibleBlock()
        iBlockNum = qBlock.blockNumber()
        qRectF = self.blockBoundingGeometry(qBlock)
        iTop = int(qRectF.translated(self.contentOffset()).top())
        iBottom = iTop + int(qRectF.height())
        iFontHeight = self.fontMetrics().height()
        iDrawWidth = self.m_LineNumArea.width() - iFontHeight * 2
        while(qBlock.isValid() and iTop <= pe.rect().bottom()):
            if qBlock.isVisible() and iBottom >= pe.rect().top():
                sTextNum, sPngAct = self.m_LineInfo.get(iBlockNum, (iBlockNum, None))
                qPainter.setPen(QtCore.Qt.black)
                qPainter.drawText(0, iTop, iDrawWidth, iFontHeight, QtCore.Qt.AlignCenter, str(sTextNum))
                if sPngAct:
                    oPngAct = GetLinePixMap(sPngAct)
                    oPngAct = oPngAct.scaled(iFontHeight, iFontHeight)
                    qPainter.drawPixmap(iDrawWidth, iTop, iFontHeight, iFontHeight, oPngAct)
                oFoldStatu = self.m_FoldStatus.get(iBlockNum, define.FOLDSTATUS.NOTHING)
                oPngFold = GetLinePixMap(oFoldStatu.value)
                oPngFold = oPngFold.scaled(iFontHeight, iFontHeight)
                qPainter.drawPixmap(iDrawWidth + iFontHeight, iTop, iFontHeight, iFontHeight, oPngFold)

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

    def JumpToPreviousMod(self):
        """跳转到上一个修改的地方"""
        self.JumpToMod(False)

    def JumpToNextMod(self):
        """跳转到上一个修改的地方"""
        self.JumpToMod(True)

    def JumpToMod(self, bNext=True):
        if not self.m_ModBlockList:
            return
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
        r = len(self.m_ModBlockList) - 1
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

    def FindWidgetMoveRight(self):
        """查找窗口移动到右侧靠边"""
        iOffset = 0
        oScroll = self.verticalScrollBar()
        if oScroll.isVisible():
            iOffset = -18
        pw = self.width() - self.m_FindWidget.width() + iOffset
        if(pw < 0):
            pw = 0
        self.m_FindWidget.move(pw, 0)

    def _CalculationFold(self):
        iLastSpaceNum = 0   # 当前空格数
        iLastLine = 0   # 记录上一次的行
        for i in range(len(self.m_SpaceNum)):
            iSpaceNum = self.m_SpaceNum[i]
            if iSpaceNum == -1:
                continue
            if iSpaceNum == iLastSpaceNum:
                iLastLine = i
                continue

            if iSpaceNum > iLastSpaceNum:   # 当有不同空格行出现，push上一次记录的行
                self.m_FoldStatus[iLastLine] = define.FOLDSTATUS.UNFOLD
                self.m_Stack.push(iLastLine)
                iLastLine = i
                iLastSpaceNum = iSpaceNum
                continue

            while(True):
                if(self.m_Stack.is_empty()):
                    break
                iLastLineNum = self.m_Stack.peek()
                iLastSpaceNum = self.m_SpaceNum[iLastLineNum]
                if(iLastSpaceNum >= iSpaceNum):
                    self.m_Stack.pop()
                    self.m_FoldBlock[iLastLineNum] = i - 1
                else:
                    break
            iLastSpaceNum = iSpaceNum
            iLastLine = i

    def LineAreaPress(self, point):
        document = self.document()
        qBlock = self.firstVisibleBlock()
        iLineNum = qBlock.firstLineNumber()
        iFontHeight = self.fontMetrics().height()
        iClickLineNum = point.y()//iFontHeight + iLineNum
        oClickBlock = document.findBlockByLineNumber(iClickLineNum)
        iBlockNum = oClickBlock.blockNumber()
        oStatue = self.m_FoldStatus.get(iBlockNum, 0)
        if not oStatue:
            return
        iEndBlockNum = self.m_FoldBlock[iBlockNum]
        if oStatue == define.FOLDSTATUS.UNFOLD:
            self._Fold(iBlockNum, iEndBlockNum)
            self.m_BindEditor()._Fold(iBlockNum, iEndBlockNum)
        elif oStatue == define.FOLDSTATUS.FOLD:
            self._UnFold(iBlockNum, iEndBlockNum)
            self.m_BindEditor()._UnFold(iBlockNum, iEndBlockNum)

    def _Fold(self, iBlockNum, iEndBlockNum):
        """折叠操作"""
        oStatue = self.m_FoldStatus.get(iBlockNum, 0)
        if oStatue == define.FOLDSTATUS.UNFOLD:
            self.m_FoldStatus[iBlockNum] = define.FOLDSTATUS.FOLD
        self._DoFold(iBlockNum, iEndBlockNum, False)

    def _UnFold(self, iBlockNum, iEndBlockNum):
        """展开操作"""
        # 展开时将子节点折叠的全展开
        for x in range(iBlockNum, iEndBlockNum + 1):
            oStatue = self.m_FoldStatus.get(x, 0)
            if oStatue == define.FOLDSTATUS.FOLD:
                self.m_FoldStatus[x] = define.FOLDSTATUS.UNFOLD
        self._DoFold(iBlockNum, iEndBlockNum, True)

    def _DoFold(self, iBlockNum, iEndBlockNum, bVisible):
        """进行展开折叠操作"""
        document = self.document()
        for x in range(iBlockNum + 1, iEndBlockNum + 1):
            oTextBlock = document.findBlockByNumber(x)
            oTextBlock.setVisible(bVisible)
        self.viewport().update()
        document.adjustSize()
        self.update()
