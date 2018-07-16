# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-11 10:51:34
@Desc: 文件系统
"""

from PyQt5 import QtWidgets, QtCore


class CMyFileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, parent=None):
        super(CMyFileSystemModel, self).__init__(parent)
        # self.m_CheckList = []
        # self.setFilter(QtCore.QDir.NoDotAndDotDot)
        self.setFilter(QtCore.QDir.Files | QtCore.QDir.AllDirs |
                       QtCore.QDir.NoDotAndDotDot)

    def columnCount(self, *args):
        return 1

    def mouseDoubleClickEvent(self, *args):
        print("1", args)


class CMyTreeView(QtWidgets.QTreeView):
    SIGNAL_CURRENT_CHANGED = QtCore.pyqtSignal(
        "PyQt_PyObject", "PyQt_PyObject")

    def __init__(self, parent=None):
        super(CMyTreeView, self).__init__(parent)

    # def mouseDoubleClickEvent(self, event):
    #     super(CMyTreeView, self).mouseDoubleClickEvent(event)
    #     print("mouseDoubleClickEvent:", event)

    def currentChanged(self, cur, pre):
        super(CMyTreeView, self).currentChanged(cur, pre)
        print("currentChanged:", cur, pre)
        self.SIGNAL_CURRENT_CHANGED.emit(cur, pre)

    def mousePressEvent(self, event):
        super(CMyTreeView, self).mousePressEvent(event)
        print("mousePressEvent:", event, self.currentIndex)

    # def currentIndex(self, event):
    #     super(CMyTreeView, self).currentIndex(event)
    #     print("currentIndex:", event)


class CMyPlainTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, *args):
        super(CMyPlainTextEdit, self).__init__(*args)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # super(CMyPlainTextEdit, self).dragEnterEvent(event)
        # tt = event.mimeData().hasFormat("text/uri-list")
        tt = event.mimeData().hasText()
        print("dragEnterEvent", tt, event)
        if(tt):
            event.acceptProposedAction()
            # event.accept()

    def dragEvent(self, event):
        # super(CMyPlainTextEdit, self).dragEvent(event)
        print("sdfdsf")
        text = event.mimeData().text()
        print("dragEnterEvent", text)

    # def dragMoveEvent(self, event):
    #     # super(CMyPlainTextEdit, self).dragMoveEvent(event)
    #     event.acceptProposedAction()
    #     print("dragMoveEvent", event)
