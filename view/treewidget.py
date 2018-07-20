# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-19 14:24:15
@Desc: 
"""

import os
import weakref

from PyQt5 import QtWidgets, QtCore, QtGui


class CMyTreeView(QtWidgets.QTreeView):

    def __init__(self, parent=None):
        super(CMyTreeView, self).__init__(parent)
        self.m_DragPosition = None
        self.m_DragItem = None

    def SetFileSystemModel(self, obj):
        self.m_FileSystemModel = weakref.ref(obj)

    def mousePressEvent(self, event):
        super(CMyTreeView, self).mousePressEvent(event)
        if(event.button() == QtCore.Qt.LeftButton):
            self.m_DragPosition = event.pos()
            index = self.indexAt(self.m_DragPosition)
            self.m_DragFile = self.m_FileSystemModel().filePath(index)

    def mouseMoveEvent(self, event):
        super(CMyTreeView, self).mousePressEvent(event)
        if(not (event.button and QtCore.Qt.LeftButton)):
            return
        if((event.pos() - self.m_DragPosition).manhattanLength() < QtWidgets.QApplication.startDragDistance()):
            return

        drag = QtGui.QDrag(self)
        oMimeData = QtCore.QMimeData()
        oMimeData.setText(self.m_DragFile)
        drag.setMimeData(oMimeData)

        pixMap = QtGui.QPixmap(120, 18)
        painter = QtGui.QPainter(pixMap)
        # file = os.path.basename(self.m_DragFile)
        # painter.drawText(QtCore.QRectF(0, 0, 120, 18), "open " + file, QtGui.QTextOption(QtCore.Qt.AlignVCenter))
        painter.drawText(QtCore.QRectF(0, 0, 120, 18), "drag", QtGui.QTextOption(QtCore.Qt.AlignVCenter))
        drag.setPixmap(pixMap)
        result = drag.exec(QtCore.Qt.MoveAction)
        del painter
        del pixMap
        del drag


class CMyFileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, parent=None):
        super(CMyFileSystemModel, self).__init__(parent)
        self.setFilter(QtCore.QDir.Files | QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)

    def columnCount(self, *args):
        return 1
