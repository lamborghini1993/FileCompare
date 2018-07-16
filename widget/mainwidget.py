# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-10 15:10:43
@Desc: 
"""

import sys
import os

from . import miscwidget, filetree, codecmpwidget, webwidget
from PyQt5 import QtWidgets, QtCore
# from ui import mainwidget_ui


class CMainWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CMainWidget, self).__init__(parent)
        self.InitUI()
        # self.InitConnect()

    def InitUI(self):
        self.m_Splitter = QtWidgets.QSplitter(self)
        self.m_FileTreeWidget = filetree.CFileTreeWidget()
        self.m_Splitter.addWidget(self.m_FileTreeWidget)

        # self.m_WebWidget = webwidget.CMyWebWidget(self)
        # self.m_WebWidget.LoadFile("E:/mygithub/FileCompare/diff.html")
        # self.m_Splitter.addWidget(self.m_WebWidget)

        self.m_CodeCmpWidget = codecmpwidget.CCodeCmpWidget()
        self.m_Splitter.addWidget(self.m_CodeCmpWidget)

        # Qt.Vertical 垂直   Qt.Horizontal 水平
        self.m_Splitter.setOrientation(QtCore.Qt.Horizontal)
        self.setCentralWidget(self.m_Splitter)

    def InitConnect(self):
        self.pushButton_ChooseDir.clicked.connect(self.ChooseDir)
        self.treeView.SIGNAL_CURRENT_CHANGED.connect(self.SelectFileChanged)

    def SelectFileChanged(self, curIndex, preIndex):
        path = self.treeView.model().filePath(curIndex)
        print("SelectFileChanged:", path, self.treeView.model())

        # print(self.treeView.currentIndex())event


def Show():
    app = QtWidgets.QApplication(sys.argv)
    obj = CMainWidget()
    obj.show()
    sys.exit(app.exec_())
