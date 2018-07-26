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


class CStack(object):
    # 初始化栈为空列表
    def __init__(self):
        self.m_Items = []

    # 判断栈是否为空，返回布尔值
    def is_empty(self):
        return self.m_Items == []

    # 返回栈顶元素
    def peek(self):
        if self.is_empty():
            return None
        return self.m_Items[self.size() - 1]

    # 返回栈的大小
    def size(self):
        return len(self.m_Items)

    # 把新的元素堆进栈里面（程序员喜欢把这个过程叫做压栈，入栈，进栈……）
    def push(self, item):
        self.m_Items.append(item)

    # 把栈顶元素丢出去（程序员喜欢把这个过程叫做出栈……）
    def pop(self):
        if self.is_empty():
            return None
        return self.m_Items.pop()

    def clear(self):
        self.m_Items = []
