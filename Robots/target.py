#! /usr/bin/python
#-*- coding: utf-8 -*-

from  Objects.robot import Robot
import math


'''
一个靶子机器人 
 
'''
class Target(Robot):

    #初始化机器人
    def init(self):
        #设置坦克的颜色（炮膛、雷达、子弹
        self.setColor(255, 0, 0)
        self.setGunColor(255, 0, 0)
        self.setRadarColor(255, 0, 0)
        self.setBulletsColor(255, 0, 0)

        #需要先设置雷达为可见，再设置雷达类型
        self.radarVisible(True) # if True the radar field is visible
        
        #get the map size
        size = self.getMapSize()
        
        self.lockRadar("gun")
        self.setRadarField("thin")
        self.inTheCorner = False
        

    
    def run(self): #main loop to command the bot
        # angle=self.getHeading() % 360
        # print ("going angle:",angle)
        # self.move(5)
        pass

    def onHitWall(self):
        pass

    def sensors(self): 
        pass
        
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        pass

    #被其他机器人撞击
    def onHitByRobot(self, robotId, robotName):
        pass

    #被子弹击中
    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        pass

    #击中敌人
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        pass

    #未击中敌人
    def onBulletMiss(self, bulletId):
        pass
        
    def onRobotDeath(self):
        pass
        
    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        pass
