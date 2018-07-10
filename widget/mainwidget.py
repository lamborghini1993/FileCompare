# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-10 15:10:43
@Desc: 
"""

import sys

from PyQt5 import QtWidgets, QtCore
from ui import mainwidget_ui


class CMainWidget(QtWidgets.QMainWindow, mainwidget_ui.Ui_MainWindow):
    def __init__(self):
        super(CMainWidget, self).__init__()
        self.setupUi(self)
        self.InitConnect()

    def InitConnect(self):
        self.pushButton_ChooseDir.clicked.connect(self.ChooseDir)

    def ChooseDir(self):
        sDir = QtWidgets.QFileDialog.getExistingDirectory(self, "选择log文件夹")
        if not sDir:
            return
        print(sDir)


def Show():
    app = QtWidgets.QApplication(sys.argv)
    obj = CMainWidget()
    obj.show()
    sys.exit(app.exec_())
