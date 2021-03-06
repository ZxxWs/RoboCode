# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import os, pickle

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, QTimer

from DeBug import DeBug
from GUI.openRobot import OpenRobot
from Objects.graph import Graph
from Ui_window import Ui_MainWindow
from battle import Battle
from editor import Editor
from Objects.robot import Robot
from RobotInfo import RobotInfo
from Objects.statistic import statistic


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.countBattle = 0  # 参加战斗的机器人个数
        self.timer = QTimer()  # QTimer是Qt中的一个定时器类，参考文档：https://doc.qt.io/qtforpython-5/PySide2/QtCore/QTimer.html

        # tableWidget是计分面板控件
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 计分板水平表头，设置格式为均匀拉直表头
        self.tableWidget.hide()  # 隐藏计分面板控件

    # 重新开始战斗
    @pyqtSlot()
    def on_pushButton_clicked(self):

        if os.path.exists(os.getcwd() + "/.datas/lastArena"):  # 获取游戏存档
            with open(os.getcwd() + "/.datas/lastArena", 'rb') as file:  # 读取游戏存档
                unpickler = pickle.Unpickler(file)  # 使用pickle包，读取存档
                dico = unpickler.load()  # dico是一个字典对象
            file.close()
        else:
            print("No last arena found.")

        # 调用下面的setUpBattle方法
        self.setUpBattle(dico["width"], dico["height"], dico["botList"])

    # 本函数被battle.py中的__init__()调用，也被上面的“重新开始战斗”调用
    def setUpBattle(self, width, height, botList):

        self.tableWidget.clearContents()  # 清理计分板的内容
        self.tableWidget.hide()  # 隐藏计分板
        self.graphicsView.show()  # 显示UI中的graphicsView控件，用于加载战斗场景
        # 设置宽、高、机器人列表
        self.width = width
        self.height = height
        self.botList = botList

        self.statisticDico = {}  # 初始化一个计分数据结构（字典类型）
        for bot in botList:
            # 填充字典计分器，键=机器人的类名，值=一个统计对象（statistic类）
            self.statisticDico[self.repres(bot)] = statistic()
        self.startBattle()  # 执行下面的开始游戏逻辑

    # 游戏开始逻辑
    def startBattle(self):

        try:
            self.timer.timeout.disconnect(self.scene.advance)

            '''
            关于del:
            由于python都是引用，而python有GC机制，所以，del语句作用在变量上，而不是数据对象上
            '''
            del self.timer
            del self.scene
            del self.sceneMenu
        except:
            pass

        self.timer = QTimer()
        self.countBattle += 1
        self.sceneMenu = QGraphicsScene()#sceneMenu为一个qt的场景对象
        self.graphicsView_2.setScene(self.sceneMenu)#graphicsView_2是UI中的一个graphicsView类型控件，(右侧显示游戏细节信息的控件
        self.scene = Graph(self, self.width, self.height)#设置场景的具体宽高
        self.graphicsView.setScene(self.scene)#将场景填充到graphicsView控件中
        self.scene.AddRobots(self.botList)  # 此函数属于graph.py中graph类的方法
        self.timer.timeout.connect(self.scene.advance)
        self.timer.start((self.horizontalSlider.value() ** 2) / 100.0)
        self.resizeEvent()

    @pyqtSlot(int)
    #战斗速度调整控件
    def on_horizontalSlider_valueChanged(self, value):

        self.timer.setInterval((value ** 2) / 100.0)

    @pyqtSlot()
    # 点击新建战斗菜单
    def on_actionNew_triggered(self):

        self.battleMenu = Battle(self)
        self.battleMenu.show()

    # 新建机器人按钮
    @pyqtSlot()
    def on_actionNew_2_triggered(self):

        self.Newrobot = Editor(self)
        self.Newrobot.show()

    @pyqtSlot()
    # 打开机器人功能
    def on_actionOpen_triggered(self):

        self.openBot = OpenRobot()
        self.openBot.show()

    def resizeEvent(self, evt=None):
        try:
            self.graphicsView.fitInView(self.scene.sceneRect(), 4)
        except:
            pass

    # 添加机器人信息，被graph.py中的Graph类的AddRobots()方法调用，
    #此处的robot参数是./Robots文件下具体的机器人类
    def addRobotInfo(self, robot):
        DeBug.debug(robot,"MainWindow","addRobotInfo")
        self.sceneMenu.setSceneRect(0, 0, 170, 800)#设置机器人细节展示控件的尺寸，左上角是0，0坐标
        rb = RobotInfo()
        rb.pushButton.setText(str(robot))
        rb.progressBar.setValue(100)
        rb.robot = robot
        robot.info = rb
        robot.progressBar = rb.progressBar
        robot.icon = rb.toolButton
        robot.icon2 = rb.toolButton_2
        p = self.sceneMenu.addWidget(rb)
        l = (len(self.scene.aliveBots))
        self.sceneMenu.setSceneRect(0, 0, 170, l * 80)
        p.setPos(0, (l - 1) * 80)

    def chooseAction(self):
        if self.countBattle >= self.spinBox.value():
            "Menu Statistic"
            self.graphicsView.hide()
            self.tableWidget.show()
            self.tableWidget.setRowCount(len(self.statisticDico))
            i = 0
            for key, value in self.statisticDico.items():
                self.tableWidget.setItem(i, 0, QTableWidgetItem(key))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(value.first)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(value.second)))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(value.third)))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(value.points)))

                i += 1

            self.countBattle = 0
            self.timer.stop()
        else:
            self.startBattle()

    # 返回机器人类名,本方法只被window.py中的MainWindow类的setUpBattle()调用过
    def repres(self, bot):

        DeBug.debug(bot, "MainWindow", "repres")

        # repr()返回一个对象内容的string格式
        # split()将字符串按照指定的分隔符切分成多个子串
        # repres:类型是一个列表 内容格式为：  ["<class 'charlier", "Charlier'>"]
        # bot:类型是：'sip.wrappertype'  内容格式为：--><class 'coin.Camper'>
        repres = repr(bot).split(".")

        return repres[1].replace("'>", "")



