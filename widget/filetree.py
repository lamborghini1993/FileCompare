# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-11 14:14:23
@Desc: 
"""

from PyQt5 import QtWidgets, QtCore
from ui import filetree_ui
from . import miscwidget


class CFileTreeWidget(QtWidgets.QWidget, filetree_ui.Ui_Form):
    def __init__(self, parent=None):
        super(CFileTreeWidget, self).__init__(parent)
        self.setupUi(self)
        self.InitConnect()
        self.show()

    def InitConnect(self):
        self.pushButton_ChooseDir.clicked.connect(self.ChooseDir)

    def ChooseDir(self):
        # sDir = QtWidgets.QFileDialog.getExistingDirectory(self, "选择log文件夹")
        # if not sDir:
        #     return
        sDir = r"E:\mygithub\FileCompare\test"
        self.m_FileSystemModel = miscwidget.CMyFileSystemModel(self)
        index = self.m_FileSystemModel.setRootPath(sDir)
        self.treeView.header().hide()
        self.treeView.setModel(self.m_FileSystemModel)
        self.treeView.setRootIndex(index)
