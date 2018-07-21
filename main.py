# -*- coding: utf-8 -*-

import os
import define

from view import mainwidget


def Start():
    if not os.path.exists(define.CACHE_DIR):
        os.makedirs(define.CACHE_DIR)
    mainwidget.Show()


if __name__ == "__main__":
    Start()
