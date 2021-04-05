# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from Ui_outPrint import Ui_Form

'''
被机器人信息类调用，用于展示一个机器人信息的细节
构造函数就是个简单从初始化
add()函数是在UI中的textEdit添加字符串msg
'''


class outPrint(QWidget, Ui_Form):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.__setUIStyle()

    def add(self, msg):
        self.textEdit.append(msg)

    # 页面UI的风格设计
    def __setUIStyle(self):
        self.setWindowModality(Qt.ApplicationModal)  # 设置其他界面不可点击
        self.setFixedSize(self.width(), self.height())  # 固定界面尺寸
        self.setStyleSheet("QWidget{background-image:url(ArtResource/backgroudBlack.png)}"
                           "QTextEdit{background:rgb(200,200,200,200);border-radius:5px;}"
                           "QTextEdit{font-size:17px;font-family:'楷体'}"
                           "QTextEdit{border-radius: 4px}"

                           )
