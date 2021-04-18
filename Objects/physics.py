#! /usr/bin/python
#-*- coding: utf-8 -*-

'''
物理类
属性：
    self.move-移动
    self.turn-转向
    self.gunTurn-炮膛的转向
    self.radarTurn-雷达的转向
    self.fire-开火
    self.currentList = []
    self.animation=动画类
    self.step-步长

方法：
    __init__
    reverse
    newAnimation
    makeAnimation
    clearAnimation
    reset
'''


class physics():
    
    def __init__(self, animation):
        
        self.move = []
        self.turn = []
        self.gunTurn = []
        self.radarTurn = []
        self.fire = []
        self.currentList = []
        self.animation = animation

        self.step = 5

    #将动画类的列表翻转
    def reverse(self):
        self.animation.list.reverse()     

    #设置新的动画
    def newAnimation(self): 
        currentList = self.makeAnimation()
        if currentList != []:
            self.animation.list.append(currentList)
            self.clearAnimation()
        

    #设置动画方法
    def makeAnimation(self ,  a = None):

        for i in range(max(len(self.move), len(self.turn), len(self.gunTurn), len(self.radarTurn), len(self.fire) )):
            try:
                m = self.move[i]
            except IndexError:
                m = 0
            try:
                t = self.turn[i]
            except IndexError:
                t = 0
            try:
                g = self.gunTurn[i]
            except IndexError:
                g = 0
            try:
                r = self.radarTurn[i]
            except IndexError:
                r = 0
            try:
                f = self.fire[i]
            except IndexError:
                f = 0
            self.currentList.append({"move": m, "turn": t, "gunTurn":g, "radarTurn":r, "fire":f})
        #reverse()函数将currentList翻转。（第一个变为最后一个，最后一个变为第一个）
        self.currentList.reverse()
        return self.currentList

    #清空动画方法
    def clearAnimation(self):
        self.move = []
        self.turn = []
        self.gunTurn = []
        self.radarTurn = []
        self.fire = []
        self.currentList = []

    #重置方法，调用清空动画，
    def reset(self):
        self.clearAnimation()
        self.animation.list = []
