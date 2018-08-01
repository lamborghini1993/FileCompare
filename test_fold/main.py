# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-27 09:55:00
@Desc: 
"""

import sys
import os
import mainwidget_ui

from PyQt5 import QtWidgets, QtCore


class CMainWidget(QtWidgets.QWidget, mainwidget_ui.Ui_Form):
    

    def __init__(self, parent=None):
        super(CMainWidget, self).__init__(parent)
        self.setupUi(self)
        self.InitConnect()

    def InitConnect(self):
        self.pushButton_Fold.clicked.connect(self.plainTextEdit.E_Fold)
        self.pushButton_Unfold.clicked.connect(self.plainTextEdit.E_Unfold)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    obj = CMainWidget()
    obj.show()
    sys.exit(app.exec_())
