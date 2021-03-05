#! /usr/bin/python
#-*- coding: utf-8 -*-

import os
import math

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QColor, QPainter


'''
子弹类
方法：
    __init__：默认初始化
    init：手动初始化（需调用）
    setColour：颜色设置
    advance：前进方式
'''
class Bullet(QGraphicsPixmapItem):      #继承Qt的QGraphicsPixmapItem类

    #默认初始化,参数为火力大小、子弹颜色、所属机器人
    def __init__(self, power, color, bot):
        QGraphicsPixmapItem.__init__(self)

        #graphics
        self.maskColor = QColor(255, 128, 0)#用Qt的QColor方法设置颜色

        self.pixmap = QPixmap(os.getcwd() + "/robotImages/blast.png")#用Qt的QPixmap方法。设置炮弹的图片
        self.setPixmap(self.pixmap)#QGraphicsPixmapItem中的方法
        self.setColour(color)#下边的自定义函数
        self.isfired = False

        #physics
        self.width = self.boundingRect().width()
        self.height = self.boundingRect().height()

        if power <=0.5:
            power = 0.5
        elif power >= 10:
            power = 10
        self.power = power
        bsize = power
        if power < 3:
            bsize = 4
        self.pixmap = self.pixmap.scaled(bsize, bsize)
        self.setPixmap(self.pixmap)#QGraphicsPixmapItem中的方法
        self.robot = bot
        
    def init(self, pos, angle, scene):

        self.angle = angle#
        self.setPos(pos)#setPos为qt中QGraphicsPixmapItem的方法，pos为一个二维坐标。x,y
        self.scene = scene
        self.isfired = True

        
    def setColour(self, color):
        mask = self.pixmap.createMaskFromColor(self.maskColor,  1)
        p = QPainter(self.pixmap)
        p.setPen(color)
        p.drawPixmap(self.pixmap.rect(), mask, mask.rect())
        p.end()
        self.setPixmap(self.pixmap)#QGraphicsPixmapItem中的方法
        self.maskColor = color


    #子弹的前进逻辑，当本类的isfired这个tag为真的时候，执行。
    def advance(self, i):

        if self.isfired:
            
            pos = self.pos()
            x = pos.x()
            y = pos.y()
            dx = - math.sin(math.radians(self.angle))*10.0
            dy = math.cos(math.radians(self.angle))*10.0
            self.setPos(x+dx, y+dy)
            if x < 0 or y < 0 or x > self.scene.width or y > self.scene.height:
                self.robot.onBulletMiss(id(self))
                self.scene.removeItem(self)
                self.robot.removeMyProtectedItem(self)

        
            
            
            
            
            
            
            
