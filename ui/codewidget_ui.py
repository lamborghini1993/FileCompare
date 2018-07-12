# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\mygithub\FileCompare\ui\codewidget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(291, 495)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_FileName = QtWidgets.QLabel(Form)
        self.label_FileName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_FileName.setObjectName("label_FileName")
        self.verticalLayout.addWidget(self.label_FileName)
        self.plainTextEdit = CMyPlainTextEdit(Form)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_FileName.setText(_translate("Form", "TextLabel"))

from widget.miscwidget import CMyPlainTextEdit
