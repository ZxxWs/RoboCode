#! /usr/bin/python
#-*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPolygonF, QColor, QBrush, QPen

'''
雷达范围类（而不是雷达，雷达指的是车身上的雷达罩子
方法：
    __init__
    setVisible：设置雷达的可见性

'''



class radarField(QGraphicsItemGroup):#继承Qt中的QGraphicsItemGroup类

    '''
    rType：雷达类型：范围、射线
    类中的item属于自定义的属性，不是父类的属性
    '''

    def __init__(self, qPointList, bot, rType):#

        QGraphicsItemGroup.__init__(self)
        self.rType = rType

        #射线类型雷达
        if rType == "poly":
            self.item = QGraphicsPolygonItem()#提供一个多边形item
            self.polygon = QPolygonF(qPointList)
            self.item.setPolygon(self.polygon)
            self.robot = bot

        #范围类型雷达
        elif rType == "round":
            self.item = QGraphicsEllipseItem()#提供一个椭圆item
            self.item.setRect(qPointList[0], qPointList[1],qPointList[2],qPointList[3])
            self.robot = bot

        color = QColor(255, 100, 6, 10)#设置雷达的颜色，
        brush = QBrush(color)
        pen = QPen(color)
        self.item.setBrush(brush)
        self.item.setPen(pen)
        self.addToGroup(self.item)
            
    #设置雷达可见性
    def setVisible(self, bol):
        if bol:
            color = QColor(255, 100, 6, 15)#四个参数分别是：R、B、G和透明度，如果雷达可见，则透明度设置为15，否则设置为0
        else:
            color = QColor(255, 100, 6, 0)
        brush = QBrush(color)
        pen = QPen(color)#QPen（钢笔）是一个基本的图形对象，用于绘制直线，曲线或者给轮廓画出矩形，椭圆形，多边形及其他形状
        self.item.setBrush(brush)
        self.item.setPen(pen)
