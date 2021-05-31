import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from GUI.Ui_deleteRobot import Ui_deleteRobot
from GUI.confirmAlert import ConfirmAlert
from GUI.editor import Editor


class DeleteRobot(QDialog, Ui_deleteRobot):
    '''
    __init__函数复用了battle中__init__的部分代码
    '''

    def __init__(self, parent=None):
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
    def on_pushButtonDelete_clicked(self):

        try:
            bot = self.listWidget.currentItem().text()  #
            self.__delRow = self.listWidget.currentRow()
            # print(self.__row)
            # print(os.getcwd() + "/Robots" + bot + '.py')

            # 删除弹框--------------------------------------
            tag = "确认删除" + bot + "机器人？"
            self.confirmAlert = ConfirmAlert(tag)  #
            self.confirmAlert.ConfirmAlertSignal.connect(self.getConfirmAlertSignal)
            self.confirmAlert.show()

        except:
            print("点击on_pushButtonOpen_clicked但未选择列表")

    # 获取ConfirmAlert界面返回的信号量
    def getConfirmAlertSignal(self, tag):  # 返回0，表示取消

        if tag == 1:
            bot = self.listWidget.currentItem().text()
            delName =str(os.getcwd() + "\\Robots\\" + bot + ".py")
            # print(delName)

            #用os库来删除文件
            os.remove(delName)
            #删除列表中的item
            self.listWidget.removeItemWidget(self.listWidget.takeItem(self.__delRow))

