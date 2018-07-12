# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\mygithub\FileCompare\ui\filetree.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(183, 453)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_ChooseDir = QtWidgets.QPushButton(Form)
        self.pushButton_ChooseDir.setObjectName("pushButton_ChooseDir")
        self.verticalLayout.addWidget(self.pushButton_ChooseDir)
        self.treeView = CMyTreeView(Form)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 20)
        self.verticalLayout.setStretch(3, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_ChooseDir.setText(_translate("Form", "选择文件夹"))

from widget.miscwidget import CMyTreeView
