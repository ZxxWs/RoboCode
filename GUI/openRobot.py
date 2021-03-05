import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from GUI.Ui_openRobot import Ui_openRobot
from GUI.editor import Editor


class OpenRobot(QDialog, Ui_openRobot):
    '''
    __init__函数复用了battle中__init__的部分代码
    '''

    def __init__(self, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.window = parent

        botnames = []  # 一个机器人列表
        botFiles = os.listdir(os.getcwd() + "/Robots")
        for bot in botFiles:
            if bot.endswith('.py'):
                # 获取文件名（除去最后一个.后的内容）
                botName = botPath = bot[:bot.rfind('.')]
                # 如果文件名字不在机器人列表中则执行以下代码
                if botName not in botnames:
                    # 将文件名字添加到机器人列表中
                    botnames.append(botName)

        ######################此处代码有缺陷：想做成文件名.类名。但只有文件名###################
        self.listWidget.addItems(botnames)

    # 确认打开按钮函数
    @pyqtSlot()
    def on_pushButtonOpen_clicked(self):

        try:
            bot = self.listWidget.currentItem().text()  #
            self.openEditor = Editor(self.window, bot + ".py")
            self.openEditor.show()
            self.close()
        except:
            print("点击on_pushButtonOpen_clicked但未选择列表")
