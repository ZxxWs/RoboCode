#! /usr/bin/python
#-*- coding: utf-8 -*-

import time, os, random

from PyQt5.QtWidgets import QGraphicsScene, QMessageBox, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QColor, QBrush
from PyQt5.QtCore import QPointF, QRectF

from DeBug import DeBug
from robot import Robot
from GUI.outPrint import outPrint


#战斗场景类
class Graph(QGraphicsScene):

    #初始化
    def __init__(self,parent, width,  height):
        QGraphicsScene.__init__(self,  parent)

        self.placeList=[]#排名列表

        self.setSceneRect(0, 0, width, height)#QGraphicsScene中的方法
        self.Parent = parent

        self.width = width#设置战场的长宽
        self.height = height

        self.grid = self.getGrid()#调用下面写的getGrid()来设置网格
        self.setTiles()#调用下面写的setTiles设置贴图

    #被window.py的MainWindow的startBattle方法调用
    def AddRobots(self, botList):

        self.aliveBots = []#生存的机器人列表
        self.deadBots = []#死亡的机器人列表
        self.allBots=botList#所有的机器人，
        try:
            posList = random.sample(self.grid, len(botList))
            for bot in botList:
                try:
                    robot = bot(self.sceneRect().size(), self, str(bot))
                    self.aliveBots.append(robot)
                    self.addItem(robot)#QGraphicsScene中的方法
                    robot.setPos(posList.pop())
                    self.Parent.addRobotInfo(robot)#这个方法是window.py中的MainWindow类的方法
                except Exception as e:
                    print("Problem with bot file '{}': {}".format(bot, str(e)))
            self.Parent.battleMenu.close()
        except ValueError:
            QMessageBox.about(self.Parent, "Alert", "Too many Bots for the map's size!")
        except AttributeError:
            pass

    #战斗结束方法，被robot调用
    def battleFinished(self):
        print("battle terminated")
        try:
            self.deadBots.append(self.aliveBots[0])
            self.removeItem(self.aliveBots[0])
        except IndexError:
            pass
        j = len(self.deadBots)

        for i in range(len(self.aliveBots)):
            self.placeList.append(repr(self.aliveBots[i]))

        self.Parent.allPlace.append(self.placeList)



        #统计战斗分数
        for i in range(j):
            print("N° {}:{}".format(j - i, self.deadBots[i]))
            if j-i == 1: #first place
                self.Parent.statisticDico[repr(self.deadBots[i])].first += 1
            if j-i == 2: #2nd place
                self.Parent.statisticDico[repr(self.deadBots[i])].second += 1
            if j-i ==3:#3rd place
                self.Parent.statisticDico[repr(self.deadBots[i])].third += 1
                
            self.Parent.statisticDico[repr(self.deadBots[i])].points += i


        self.Parent.chooseAction()       

    #设置瓷砖的方法(设置贴图方法)

    #设置战场贴图
    def setTiles(self):

        #background
        brush = QBrush()#QBrush(画刷)是一个基本的图形对象，用于填充如矩形，椭圆形，多边形等形状，QBrush有三种类型，预定义，过渡，和纹理图案
        pix = QPixmap(os.getcwd() + "/robotImages/tile.png")
        brush.setTexture(pix)
        brush.setStyle(24)
        self.setBackgroundBrush(brush)
        
        #wall：left、right、top、bottom都是QGraphicsRectItem类型
        #left
        left = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileVert.png")#获取贴图
        left.setRect(QRectF(0, 0, pix.width(), self.height))#尺寸：宽是图片宽度 ，高度是战场高度
        brush.setTexture(pix)#设置贴图函数
        brush.setStyle(24)#参数24指平铺格式（参数为枚举类型）详情见 https://doc.qt.io/qt-5/qt.html#BrushStyle-enum
        left.setBrush(brush)
        left.name = 'left'
        self.addItem(left)

        #right
        right = QGraphicsRectItem()
        right.setRect(self.width - pix.width(), 0, pix.width(), self.height)#尺寸：宽是图片的宽度、高是战场的高
        right.setBrush(brush)
        right.name = 'right'
        self.addItem(right)

        #top
        top = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileHori.png")
        top.setRect(QRectF(0, 0, self.width, pix.height()))
        brush.setTexture(pix)
        brush.setStyle(24)
        top.setBrush(brush)
        top.name = 'top'
        self.addItem(top)

        #bottom
        bottom = QGraphicsRectItem()
        bottom.setRect(0 ,self.height - pix.height() , self.width, pix.height())
        bottom.setBrush(brush)
        bottom.name = 'bottom'
        self.addItem(bottom)



    #获取网格函数，
    #-----------------------------------------------------------------作用未知、、、、
    def getGrid(self):
        w = int(self.width/80)
        h = int(self.height/80)
        l = []
        for i in range(w):
            for j in range(h):
                l.append(QPointF((i+0.5)*80, (j+0.5)*80))#QPointF也是一个点坐标类，只是坐标为浮点数，，可以通过x(),y()等函数方便的进行存取操作，另外也重载了大量的运算符，

        return l
