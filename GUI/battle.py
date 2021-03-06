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


    def __init__(self, parent=None):

        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.window = parent#战斗类的（父亲）参数是window类
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
            #向listWidget控件中添加机器人名字,其中key类型为字符串
            self.listWidget.addItem(key)
            DeBug.debug(key,"battle","__init__")


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


        # 保存本次战斗，在开始游戏按钮中就执行保存游戏记录
        self.save(width, height, botList)
        self.window.setUpBattle(width, height, botList)  # 调用父界面的setUpBattle函数


    #保存游戏
    def save(self, width, height, botList):

        dico = {}#游戏存档为一个字典对象，其属性为下面三个：宽、高、机器人列表
        dico["width"] = width
        dico["height"] = height
        dico["botList"] = botList

        #如果项目中不存在存档目录，则创建一个
        if not os.path.exists(os.getcwd() + "/.datas/"):
            os.makedirs(os.getcwd() + "/.datas/")

        #打开游戏存档文件
        with open(os.getcwd() + "/.datas/lastArena", 'wb') as file:

            #构造一个pickler对象
            pickler = pickle.Pickler(file)

            #pickle.dump(obj, file[, protocol]) 序列化对象，并将结果数据流写入到文件对象中。参数protocol是序列化模式，默认值为0，表示以文本的形式序列化。protocol的值还可以是1或2，表示以二进制的形式序列化。
            pickler.dump(dico)

        #关闭文件
        file.close()
