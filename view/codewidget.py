# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-19 14:02:33
@Desc: 代码对比的控件
"""

import weakref
import time
import os

from PyQt5 import QtWidgets, QtCore, QtGui


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
    CLEAR_PLAIN_TEXT_EDIT = QtCore.pyqtSignal()

    def __init__(self, *args):
        super(CCodeEdit, self).__init__(*args)
        self.m_BindEditor = None
        self.m_BindLabel = None
        self.m_LineNum = 0      # 代码的行数
        self.m_LineInfo = {}    # 真实行号:(原来行号,行首变化行为)
        self.m_BlockBgInfo = {}  # 真实行号:每行的颜色
        self.m_bDragIn = False
        self.m_CurFile = None
        self.m_LineNumArea = CLineNumArea(self)
        self.m_ScrollBar = CScrollBar(self)
        self.InitUI()
        self.InitConnect()

    def InitUI(self):
        self.setVerticalScrollBar(self.m_ScrollBar)
        self.setTabStopWidth(self.fontMetrics().width("_") * 4)
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setReadOnly(True)
        self.UpdateLineNumAreaWidth(0)
        self.SetShowTabAndSpaces(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setAcceptDrops(True)

    def InitConnect(self):
        self.blockCountChanged.connect(self.UpdateLineNumAreaWidth)
        self.updateRequest.connect(self.UpdateLineNumArea)

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

    def UpdateLineNumAreaWidth(self, _):
        self.setViewportMargins(self.LineNumAreaWidth() + 20, 0, 0, 0)

    def UpdateLineNumArea(self, qRect, iDy):
        if iDy:
            self.m_LineNumArea.scroll(0, iDy)
        else:
            self.m_LineNumArea.update(0, qRect.y(), self.m_LineNumArea.width(), qRect.height())
        if qRect.contains(self.viewport().rect()):
            self.UpdateLineNumAreaWidth(0)

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
        self.m_BindLabel().setText(os.path.basename(self.m_CurFile))
        self.CLEAR_PLAIN_TEXT_EDIT.emit()

    def SplitFileByFrame(self, file):
        pass
