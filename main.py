# -*- coding: utf-8 -*-

import os
import time
import logging
import define

from view import mainwidget
from lib import misc


def InitConfig():
    handler = logging.FileHandler(filename=define.LOG_FILE, mode='a', encoding="utf-8")
    handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    logger.addHandler(ch)


def ClearOldLog():
    """清理超过10000行的log内容"""
    if not os.path.isfile(define.LOG_FILE):
        return
    with open(define.LOG_FILE, "r", encoding="utf8") as of:
        lstLine = of.readlines()
        lstNewLine = lstLine[-10000:]
    with open(define.LOG_FILE, "w", encoding="utf8") as of:
        of.writelines(lstNewLine)


def Show():
    try:
        mainwidget.Show()
    except Exception as e:
        misc.PythonError()


def Start():
    InitConfig()
    ClearOldLog()
    Show()


if __name__ == "__main__":
    Start()
