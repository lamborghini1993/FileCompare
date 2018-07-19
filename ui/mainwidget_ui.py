# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\mygithub\FileCompare\ui\mainwidget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1407, 826)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_Up = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Up.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Up.setFont(font)
        self.pushButton_Up.setAutoFillBackground(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/app/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Up.setIcon(icon)
        self.pushButton_Up.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Up.setObjectName("pushButton_Up")
        self.horizontalLayout.addWidget(self.pushButton_Up)
        self.pushButton_Down = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Down.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Down.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/app/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Down.setIcon(icon1)
        self.pushButton_Down.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Down.setObjectName("pushButton_Down")
        self.horizontalLayout.addWidget(self.pushButton_Down)
        self.pushButton_Find = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Find.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Find.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/app/find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Find.setIcon(icon2)
        self.pushButton_Find.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Find.setObjectName("pushButton_Find")
        self.horizontalLayout.addWidget(self.pushButton_Find)
        self.pushButton_Jump = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Jump.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Jump.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/app/jump.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Jump.setIcon(icon3)
        self.pushButton_Jump.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_Jump.setObjectName("pushButton_Jump")
        self.horizontalLayout.addWidget(self.pushButton_Jump)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_ChooseDir = QtWidgets.QPushButton(self.widget)
        self.pushButton_ChooseDir.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_ChooseDir.setFont(font)
        self.pushButton_ChooseDir.setObjectName("pushButton_ChooseDir")
        self.verticalLayout_3.addWidget(self.pushButton_ChooseDir)
        self.treeView = CMyTreeView(self.widget)
        self.treeView.setObjectName("treeView")
        self.verticalLayout_3.addWidget(self.treeView)
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter_2 = QtWidgets.QSplitter(self.widget_2)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.widget_4 = QtWidgets.QWidget(self.splitter_2)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_left = QtWidgets.QLabel(self.widget_4)
        self.label_left.setAlignment(QtCore.Qt.AlignCenter)
        self.label_left.setObjectName("label_left")
        self.verticalLayout_5.addWidget(self.label_left)
        self.plainTextEdit_left = CCodeEdit(self.widget_4)
        self.plainTextEdit_left.setReadOnly(True)
        self.plainTextEdit_left.setObjectName("plainTextEdit_left")
        self.verticalLayout_5.addWidget(self.plainTextEdit_left)
        self.widget_5 = QtWidgets.QWidget(self.splitter_2)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_right = QtWidgets.QLabel(self.widget_5)
        self.label_right.setAlignment(QtCore.Qt.AlignCenter)
        self.label_right.setObjectName("label_right")
        self.verticalLayout_6.addWidget(self.label_right)
        self.plainTextEdit_right = CCodeEdit(self.widget_5)
        self.plainTextEdit_right.setReadOnly(True)
        self.plainTextEdit_right.setObjectName("plainTextEdit_right")
        self.verticalLayout_6.addWidget(self.plainTextEdit_right)
        self.verticalLayout_4.addWidget(self.splitter_2)
        self.widget_3 = QtWidgets.QWidget(self.splitter)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBox_start = QtWidgets.QSpinBox(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_start.setFont(font)
        self.spinBox_start.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_start.setObjectName("spinBox_start")
        self.gridLayout.addWidget(self.spinBox_start, 0, 1, 1, 1)
        self.spinBox_end = QtWidgets.QSpinBox(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_end.setFont(font)
        self.spinBox_end.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_end.setObjectName("spinBox_end")
        self.gridLayout.addWidget(self.spinBox_end, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_2.setStretch(0, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBox = QtWidgets.QComboBox(self.widget_3)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setEditable(True)
        self.comboBox.setCurrentText("")
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.widget_3)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/app/del.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon4)
        self.pushButton.setIconSize(QtCore.QSize(30, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.textEdit = QtWidgets.QTextEdit(self.widget_3)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.pushButton_compare = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_compare.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_compare.setFont(font)
        self.pushButton_compare.setObjectName("pushButton_compare")
        self.verticalLayout.addWidget(self.pushButton_compare)
        self.verticalLayout_2.addWidget(self.splitter)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1407, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Up.setText(_translate("MainWindow", "上一个"))
        self.pushButton_Down.setText(_translate("MainWindow", "下一个"))
        self.pushButton_Find.setText(_translate("MainWindow", "查找"))
        self.pushButton_Jump.setText(_translate("MainWindow", "跳转"))
        self.pushButton_ChooseDir.setText(_translate("MainWindow", "选择文件夹"))
        self.label_left.setText(_translate("MainWindow", "TextLabel"))
        self.label_right.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "起始帧:"))
        self.label_2.setText(_translate("MainWindow", "结束帧:"))
        self.label_3.setText(_translate("MainWindow", "选择过滤方案:"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "使用python的正则匹配过滤规则，每一行代表一种过滤"))
        self.pushButton_compare.setText(_translate("MainWindow", "开始对比"))

from view.codewidget import CCodeEdit
from view.treewidget import CMyTreeView
import res_rc
