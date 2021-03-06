# -*- coding: utf-8 -*-

"""
Module implementing RobotInfo.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot

from outPrint import outPrint
from Ui_RobotInfo import Ui_Form

'''
机器人信息类：继承于Qt的QWidget和一个自定义UI(UI_RobotInfo)
方法：
    __init__():构造方法
    on_pushButton_clicked：按钮点击方法
    on_progressBar_valueChanged：血量条改变方法
'''


class RobotInfo(QWidget, Ui_Form):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.out = outPrint()  # 初始化一个信息输出UI对象

    @pyqtSlot()
    def on_pushButton_clicked(self):

        self.out.setWindowTitle(str(self.robot))
        self.out.show()  # 打开信息输出UI对象

    @pyqtSlot(int)
    # 设置血量条颜色
    def on_progressBar_valueChanged(self, value):

        value -= 7
        if value <= 0:
            value = 0

        # 根据值来设置RGB的值
        if value >= 50:
            green = 255
            red = int(510 - (value * 2) * 2.55)
        else:
            red = 255
            green = int((value * 2) * 2.55)

        self.progressBar.setStyleSheet("""
        QProgressBar {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
        height: 5px;
        }
        QProgressBar::chunk {
        background-color: rgb(""" + str(red) + "," + str(green) + """,0);
        }
        """)
