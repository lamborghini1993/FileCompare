# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-18 20:29:41
@Desc: 样式
"""

QSS = """
    QWidget {
        font-family: "微软雅黑";
        border-width: 1px;
        border-color: $background5;
    }
    QScrollBar::vertical {
        margin: 0px;
        background-color: $background5;
        border: 0px;
        width: 4px;
    }
    QPlainTextEdit {
        font-family: "Consolas";
    }
    QComboBox, QLineEdit, QSpinBox, QTextEdit, QListView, QPlainTextEdit {
        background-color: $background6;
        selection-color: $background1;
        selection-background-color: $background2;
    }
    QMainWindow, QDialog {
        background-color: $background3;
        border-style: solid;
    }
    QPushButton {
        color: $background6;
        background-color: $background4;
        border-style: solid;
    }
    QPushButton:hover {
        color: #000000;
        background-color: #B9D7FC;
        border-style: solid;
    }
    QPushButton:pressed {
        color: $background6;
        background-color: #587D88;
        border-style: solid;
    }
    QPushButton:pressed {
        color: $#948D2C;
        background-color: #CCCCCC;
        border-style: solid;
    }
"""


COLOR = {
    "$background1":     "#0A214C",
    "$background2":     "#C19A6B",
    "$background3":     "#99D9EA",
    "$background4":     "#7092BE",
    "$background5":     "#00A2E8",
    "$background6":     "#FFFFFF",
}


def GetSytle():
    qss = QSS
    for sFlag, sColor in COLOR.items():
        qss = qss.replace(sFlag, sColor)
    return qss
