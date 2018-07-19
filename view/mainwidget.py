# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-10 15:10:43
@Desc: 
"""

import sys
import os
import res_rc

from PyQt5 import QtWidgets, QtCore
from ui import mainwidget_ui
from lib import style


class CMainWidget(QtWidgets.QMainWindow, mainwidget_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(CMainWidget, self).__init__(parent)
        self.setupUi(self)
        self.InitUI()
        self.InitConnect()

    def InitUI(self):
        self.setStyleSheet(style.GetSytle())
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 8)
        self.splitter.setStretchFactor(2, 2)

    def InitConnect(self):
        pass


def Show():
    app = QtWidgets.QApplication(sys.argv)
    obj = CMainWidget()
    obj.show()
    sys.exit(app.exec_())
