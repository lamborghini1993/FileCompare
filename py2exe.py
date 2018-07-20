#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil

sCurPath = os.getcwd()

Name = "FrameDebug"
sCmd = "pyinstaller -w \
-n %s \
-i=./ui/png/main.ico \
-D ./main.py" % (Name)

os.system(sCmd)


soucre = os.path.join(os.getcwd(), "dist", Name)
distination = os.path.join(os.getcwd(), Name)
if os.path.exists(distination):
    shutil.rmtree(distination)
shutil.move(soucre, distination)
shutil.rmtree("build")
shutil.rmtree("dist")
os.remove("%s.spec" % Name)
