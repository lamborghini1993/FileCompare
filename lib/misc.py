# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-07-19 16:47:10
@Desc: 存放公共函数
"""

import json
import os


def JsonDump(data, path, **myArgs):
    jsonArgs = {
        "ensure_ascii": False,
        "allow_nan": False,
        "indent": 4,
    }
    jsonArgs.update(myArgs)
    bDone = False
    fp = None
    coding = jsonArgs.pop("encoding", "utf-8")
    try:
        fp = open(path, "w", encoding=coding)
        json.dump(data, fp, **jsonArgs)
        bDone = True
    except:
        pass
    if fp:
        fp.close()
    return bDone


def JsonLoad(path, default=None, **jsonArgs):
    if not os.path.exists(path):
        return default
    coding = jsonArgs.pop("encoding", "utf-8")
    fp = None
    try:
        fp = open(path, "r", encoding=coding)
        default = json.load(fp, **jsonArgs)
    except:
        pass
    if fp:
        fp.close()
    return default
