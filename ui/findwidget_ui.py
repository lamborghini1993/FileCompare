# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\mygithub\FileCompare\ui\findwidget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 47)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_CaseSensitively = QtWidgets.QPushButton(Form)
        self.pushButton_CaseSensitively.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_CaseSensitively.setFont(font)
        self.pushButton_CaseSensitively.setObjectName("pushButton_CaseSensitively")
        self.horizontalLayout.addWidget(self.pushButton_CaseSensitively)
        self.pushButton_WholeWords = QtWidgets.QPushButton(Form)
        self.pushButton_WholeWords.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_WholeWords.setFont(font)
        self.pushButton_WholeWords.setObjectName("pushButton_WholeWords")
        self.horizontalLayout.addWidget(self.pushButton_WholeWords)
        self.pushButton_Regular = QtWidgets.QPushButton(Form)
        self.pushButton_Regular.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Regular.setFont(font)
        self.pushButton_Regular.setObjectName("pushButton_Regular")
        self.horizontalLayout.addWidget(self.pushButton_Regular)
        self.pushButton_Pre = QtWidgets.QPushButton(Form)
        self.pushButton_Pre.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Pre.setFont(font)
        self.pushButton_Pre.setObjectName("pushButton_Pre")
        self.horizontalLayout.addWidget(self.pushButton_Pre)
        self.pushButton_Next = QtWidgets.QPushButton(Form)
        self.pushButton_Next.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Next.setFont(font)
        self.pushButton_Next.setObjectName("pushButton_Next")
        self.horizontalLayout.addWidget(self.pushButton_Next)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEdit.setPlaceholderText(_translate("Form", "输入关键词查找"))
        self.pushButton_CaseSensitively.setToolTip(_translate("Form", "区分大小写(Alt+C)"))
        self.pushButton_CaseSensitively.setText(_translate("Form", "Aa"))
        self.pushButton_WholeWords.setToolTip(_translate("Form", "全字匹配(Alt+W)"))
        self.pushButton_WholeWords.setText(_translate("Form", "Ab"))
        self.pushButton_Regular.setToolTip(_translate("Form", "正则匹配(Alt+R)"))
        self.pushButton_Regular.setText(_translate("Form", ".*"))
        self.pushButton_Pre.setToolTip(_translate("Form", "上一处匹配(Shift+F3)"))
        self.pushButton_Pre.setText(_translate("Form", "↑"))
        self.pushButton_Next.setToolTip(_translate("Form", "下一处匹配(F3)"))
        self.pushButton_Next.setText(_translate("Form", "↓"))

