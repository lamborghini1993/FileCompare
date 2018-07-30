# -*- coding: utf-8 -*-

import os
import time
import logging
import define

from view import mainwidget
from lib import misc


def MakeDir():
    """创建文件夹"""
    if not os.path.exists(define.CACHE_DIR):
        os.makedirs(define.CACHE_DIR)


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


def ClearOldCache():
    """清理超过一周的缓存文件"""
    iNow = time.time()
    for sFile in os.listdir(define.CACHE_DIR):
        path = os.path.join(define.CACHE_DIR, sFile)
        if(iNow - os.path.getmtime(path) > 7 * 24 * 3600):
            os.remove(path)


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
    MakeDir()
    InitConfig()
    ClearOldLog()
    ClearOldCache()
    Show()


if __name__ == "__main__":
    Start()
