#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/10/30 3:55 下午
# @Author  : Rex
# 程序主入口
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from testToolsKit.UI.startDownload import Ui_MainWindow

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("../Pictures/ImageReady.png"))
ex = Ui_MainWindow()
sys.exit(app.exec_())
