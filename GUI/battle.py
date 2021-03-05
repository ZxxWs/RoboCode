# -*- coding: utf-8 -*-

import os
import pickle

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from DeBug import DeBug
from Objects.robot import Robot
from Ui_battle import Ui_Dialog

'''用于战斗的创建、打开以及保存等'''


class Battle(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.window = parent
        botnames = []  # 一个机器人列表
        self.listBots = {}  # 一个机器人字典
        # 获取Robots文件下的文件列表
        botFiles = os.listdir(os.getcwd() + "/Robots")

        for botFile in botFiles:
            # 如果文件尾缀为.py则执行以下代码
            if botFile.endswith('.py'):
                # 获取文件名（除去最后一个.后的内容）
                botName = botPath = botFile[:botFile.rfind('.')]
                # 如果文件名字不在机器人列表中则执行以下代码
                if botName not in botnames:
                    # 将文件名字添加到机器人列表中
                    botnames.append(botName)
                    try:
                        # 使用的是一个动态导入方法
                        botModule = __import__(botPath)

                        # dir(botModule)是将botModule模块中的标识符(属性）转化为列表
                        for name in dir(botModule):

                            if botName == "T800":
                                DeBug.debug(type(getattr(botModule, name)))

                            # getattr()这个方法最主要的作用是实现反射机制
                            # __subclasses__()函数获取类的所有子类
                            if getattr(botModule, name) in Robot.__subclasses__():
                                someBot = getattr(botModule, name)
                                bot = someBot

                                self.listBots[str(bot).replace("<class '", "").replace("'>", "")] = bot
                                break
                    except Exception as e:
                        print("Problem with bot file '{}': {}".format(botFile, str(e)))

        for key in self.listBots.keys():
            self.listWidget.addItem(key)

    @pyqtSlot()
    # 添加机器人按钮函数
    def on_pushButton_clicked(self):
        self.listWidget_2.addItem(self.listWidget.currentItem().text())

    @pyqtSlot()
    # 移除机器人按钮函数
    def on_pushButton_2_clicked(self):
        item = self.listWidget_2.takeItem(self.listWidget_2.currentRow())
        item = None

    # 开始按钮函数
    @pyqtSlot()
    def on_pushButton_3_clicked(self):

        width = self.spinBox.value()  # 获取战场尺寸
        height = self.spinBox_2.value()
        botList = []
        for i in range(self.listWidget_2.count()):
            key = str(self.listWidget_2.item(i).text())
            botList.append(self.listBots[key])

        self.save(width, height, botList)  # 保存本次战斗
        self.window.setUpBattle(width, height, botList)  # 调用父界面的setUpBattle函数

    def save(self, width, height, botList):
        dico = {}
        dico["width"] = width
        dico["height"] = height
        dico["botList"] = botList

        if not os.path.exists(os.getcwd() + "/.datas/"):
            os.makedirs(os.getcwd() + "/.datas/")

        with open(os.getcwd() + "/.datas/lastArena", 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(dico)
        file.close()
