# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwidget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(344, 466)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_Fold = QtWidgets.QPushButton(Form)
        self.pushButton_Fold.setObjectName("pushButton_Fold")
        self.horizontalLayout.addWidget(self.pushButton_Fold)
        self.pushButton_Unfold = QtWidgets.QPushButton(Form)
        self.pushButton_Unfold.setObjectName("pushButton_Unfold")
        self.horizontalLayout.addWidget(self.pushButton_Unfold)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.plainTextEdit = CMyText(Form)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_Fold.setText(_translate("Form", "折叠(11-50行)"))
        self.pushButton_Unfold.setText(_translate("Form", "展开"))

from mytext import CMyText
