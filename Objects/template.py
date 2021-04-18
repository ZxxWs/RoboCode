#! /usr/bin/python
# -*- coding: utf-8 -*-

from robot import Robot

'''
机器人模板类
'''

class Template(Robot):

    # 初始化
    def init(self):
        # 设置坦克的颜色（炮膛、雷达、子弹
        self.setColor(255, 0, 0)
        self.setGunColor(255, 0, 0)
        self.setRadarColor(255, 0, 0)
        self.setBulletsColor(255, 0, 0)

        self.radarVisible(True)
        size = self.getMapSize()

        self.lockRadar("gun")
        self.setRadarField("thin")
        self.inTheCorner = False

    #--------------以下函数必须有--------------
    def run(self):
        pass

    def onHitWall(self):
        pass

    def sensors(self):
        pass

    def onRobotHit(self, robotId, robotName):
        pass

    def onHitByRobot(self, robotId, robotName):
        pass

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower):
        pass

    def onBulletHit(self, botId, bulletId):
        pass

    def onBulletMiss(self, bulletId):
        pass

    def onRobotDeath(self):
        pass

    def onTargetSpotted(self, botId, botName, botPos):
        pass
