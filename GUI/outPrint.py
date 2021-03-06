# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

from Ui_outPrint import Ui_Form



'''
被机器人信息类调用，用于展示一个机器人信息的细节
构造函数就是个简单从初始化
add()函数是在UI中的textEdit添加字符串msg
'''
class outPrint(QWidget, Ui_Form):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        self.setupUi(self)

        
    def add(self, msg):
        self.textEdit.append(msg)
