# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-19 14:24:15
@Desc: 
"""

from PyQt5 import QtWidgets, QtCore


class CMyTreeView(QtWidgets.QTreeView):
    SIGNAL_CURRENT_CHANGED = QtCore.pyqtSignal(
        "PyQt_PyObject", "PyQt_PyObject")

    def __init__(self, parent=None):
        super(CMyTreeView, self).__init__(parent)

    # def mouseDoubleClickEvent(self, event):
    #     super(CMyTreeView, self).mouseDoubleClickEvent(event)
    #     print("mouseDoubleClickEvent:", event)

    # def currentChanged(self, cur, pre):
    #     super(CMyTreeView, self).currentChanged(cur, pre)
    #     print("currentChanged:", cur, pre)
    #     self.SIGNAL_CURRENT_CHANGED.emit(cur, pre)

    # def mousePressEvent(self, event):
    #     super(CMyTreeView, self).mousePressEvent(event)
    #     print("mousePressEvent:", event, self.currentIndex)

    # def currentIndex(self, event):
    #     super(CMyTreeView, self).currentIndex(event)
    #     print("currentIndex:", event)


class CMyFileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, parent=None):
        super(CMyFileSystemModel, self).__init__(parent)
        self.setFilter(QtCore.QDir.Files | QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)

    def columnCount(self, *args):
        return 1

    def mouseDoubleClickEvent(self, *args):
        # print("1", args)
        pass
