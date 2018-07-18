# -*- coding: utf-8 -*-

import os
import sys

lstIgnore = [".git", ".vscode", "__pycache__", "mytool", "log"]

def IsIgnore(sDir):
    for sTmp in lstIgnore:
        if sDir.find(sTmp) != -1:
            return True
    return False

for sDir, lstDir, lstFile in os.walk(os.getcwd()):
    if IsIgnore(sDir):
        continue
    for sFile in lstFile:
        if sFile.endswith(".ui"):
            sUIFile = os.path.join(sDir, sFile)
            sPYFile = sUIFile[:-3] + "_ui.py"
            os.system("pyuic5 -o %s %s" % (sPYFile, sUIFile))
            print("%s   ->    %s" %(sUIFile, sPYFile))
        if sFile.endswith(".qrc"):
            sQrcFile = os.path.join(sDir, sFile)
            sPYFile = sQrcFile[:-4] + "_rc.py"
            os.system("pyrcc5 -o %s %s" % (sPYFile, sQrcFile))
            print("%s   ->    %s" %(sQrcFile, sPYFile))
