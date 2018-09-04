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
    handler = logging.FileHandler(filename=define.LOG_FILE, mode='a', encoding="utf-8")
    handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
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


def Start():
    MakeDir()
    InitConfig()
    ClearOldLog()
    ClearOldCache()
    mainwidget.Show()


if __name__ == "__main__":
    try:
        Start()
    except Exception as e:
        misc.PythonError()
