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
        border-color: $background10;
    }
    QScrollBar::vertical {
        margin: 0px;
        background-color: $background10;
        border: 0px;
        width: 4px;
    }
    QPlainTextEdit {
        font-family: "Consolas";
    }
    QComboBox, QLineEdit, QSpinBox, QTextEdit, QListView, QPlainTextEdit {
        background-color: $background6;
        selection-color: $background11;
        selection-background-color: $background12;
    }
    QDialog, QMainWindow {
        background-color: $background13;
        border-style: solid;
    }
    QPushButton {
        color: $background6;
        background-color: $background14;
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
    "$background1":   "#3A5FBC",
    "$background2":   "#3D7FDD",
    "$background3":   "#80B7F4",
    "$background4":   "#F5FAFE",
    "$background5":   "#80B7F4",
    "$background6":   "#FFFFFF",
    "$foreground1":   "#F5FAFE",
    "$foreground2":   "#111111",
    "$foreground3":   "#EdF5FE",

    "$background10":    "#00A2E8",
    "$background11":    "#0A214C",
    "$background12":    "#C19A6B",
    "$background13":    "#99D9EA",
    "$background14":    "#7092BE",
}


def GetSytle():
    qss = QSS
    for sFlag, sColor in COLOR.items():
        qss = qss.replace(sFlag, sColor)
    return qss
