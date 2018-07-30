# -*- coding: utf-8 -*-

import os
import time
import logging
import define

# from widget import mainwidget
from view import mainwidget
from lib import misc


def InitConfig():
    logging.basicConfig(
        filename=define.LOG_FILE,
        format="[%(asctime)s] (%(levelname)s) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
        filemode="a",
    )
    ch = logging.StreamHandler()
    logger = logging.getLogger()
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
    except:
        misc.PythonError()


def Start():
    InitConfig()
    ClearOldLog()
    Show()


if __name__ == "__main__":
    Start()
