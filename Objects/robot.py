import time, os, math
import traceback

from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QColor, QPainter, QIcon
from PyQt5.QtCore import QPointF

from physics import physics
from bullet import Bullet
from radarField import radarField
from animation import animation

'''
QGraphicsItemGroup继承QGraphicsItem类
Robot类：
    属性： 
    

'''


class Robot(QGraphicsItemGroup):

    def __init__(self, mapSize, parent, repr):
        QGraphicsItemGroup.__init__(self)

        # 公有属性
        self.gamePlace = 1

        # 私有属性
        self.__mapSize = mapSize
        self.__parent = parent
        self.__health = 100
        self.__repr = repr

        self.__gunLock = "free"
        self.__radarLock = "Free"#字面意思是雷达锁

        # 两个动画对象、一个physics对象
        self.__runAnimation = animation("run")
        self.__targetAnimation = animation("target")
        self.__physics = physics(self.__runAnimation)  # 一个physics对象

        # --------------------------------------未懂(mask 图画颜色)--------------------------
        self.maskColor = QColor(0, 255, 255)
        self.gunMaskColor = QColor(0, 255, 255)  # 炮膛颜色
        self.radarMaskColor = QColor(0, 255, 255)  # 雷达颜色

        # 加载图片
        self.__base = QGraphicsPixmapItem()
        self.__base.pixmap = QPixmap(os.getcwd() + "/robotImages/baseGrey.png")
        self.__base.setPixmap(self.__base.pixmap)
        self.addToGroup(self.__base)  # 本类中第一次执行addToGroup
        self.__baseWidth = self.__base.boundingRect().width()
        self.__baseHeight = self.__base.boundingRect().height()

        # 加载炮膛图片
        self.__gun = QGraphicsPixmapItem()
        self.__gun.pixmap = QPixmap(os.getcwd() + "/robotImages/gunGrey.png")
        self.__gun.setPixmap(self.__gun.pixmap)
        self.addToGroup(self.__gun)
        self.__gunWidth = self.__gun.boundingRect().width()
        self.__gunHeight = self.__gun.boundingRect().height()

        # 炮膛位置
        x = self.__base.boundingRect().center().x()
        y = self.__base.boundingRect().center().y()
        self.__gun.setPos(x - self.__gunWidth / 2.0, y - self.__gunHeight / 2.0)



        #--------------------------雷达初始化-----------------------------

        # 加载雷达图片
        self.__radar = QGraphicsPixmapItem()
        self.__radar.pixmap = QPixmap(os.getcwd() + "/robotImages/radar.png")
        self.__radar.setPixmap(self.__radar.pixmap)
        self.addToGroup(self.__radar)
        self.__radarWidth = self.__radar.boundingRect().width()
        self.__radarHeight = self.__radar.boundingRect().height()
        # radar position
        self.__radar.setPos(x - self.__radarWidth / 2.0, y - self.__radarHeight / 2.0)

        # 加载雷达范围
        firstPoint = QPointF(x - self.__radarWidth / 2, y)
        secondPoint = QPointF(x + self.__radarWidth / 2, y)
        thirdPoint = QPointF(x + 4 * self.__radarWidth, y + 700)
        fourthPoint = QPointF(x - 4 * self.__radarWidth, y + 700)
        qPointListe = []
        qPointListe.append(firstPoint)
        qPointListe.append(secondPoint)
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        self.__radarField = radarField(qPointListe, self, "poly")

        # 大雷达范围
        qPointListe.remove(fourthPoint)
        qPointListe.remove(thirdPoint)
        thirdPoint = QPointF(x + 10 * self.__radarWidth, y + 400)
        fourthPoint = QPointF(x - 10 * self.__radarWidth, y + 400)
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        self.__largeRadarField = radarField(qPointListe, self, "poly")

        # 细雷达范围
        qPointListe.remove(fourthPoint)
        qPointListe.remove(thirdPoint)
        thirdPoint = QPointF(x + 0.4 * self.__radarWidth, y + 900)
        fourthPoint = QPointF(x - 0.4 * self.__radarWidth, y + 900)
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        self.__thinRadarField = radarField(qPointListe, self, "poly")

        # 弧形雷达范围
        self.__roundRadarField = radarField([0, 0, 300, 300], self, "round")
        self.addToGroup(self.__roundRadarField)
        self.__roundRadarField.setPos(x - self.__roundRadarField.boundingRect().width() / 2.0,
                                      y - self.__roundRadarField.boundingRect().height() / 2.0)

        # add to group
        self.addToGroup(self.__radarField)
        self.addToGroup(self.__largeRadarField)
        self.addToGroup(self.__thinRadarField)

        #一个坦克上有三个雷达范围，但初始化的时候都是隐藏的
        self.__largeRadarField.hide()
        self.__thinRadarField.hide()
        self.__roundRadarField.hide()
        #--------------------------雷达初始化（上-----------------------------

        # 设置坦克颜色：RGB
        self.setColor(0, 200, 100)
        self.setGunColor(0, 200, 100)
        self.setRadarColor(0, 200, 100)
        self.setBulletsColor(0, 200, 100)

        # 设置原点:
        # 雷达范围
        self.__radarField.setTransformOriginPoint(x, y)
        self.__largeRadarField.setTransformOriginPoint(x, y)
        self.__thinRadarField.setTransformOriginPoint(x, y)
        # 车身
        x = self.__baseWidth / 2
        y = self.__baseHeight / 2
        self.__base.setTransformOriginPoint(x, y)
        # 炮膛
        x = self.__gunWidth / 2
        y = self.__gunHeight / 2
        self.__gun.setTransformOriginPoint(x, y)
        # 雷达
        x = self.__radarWidth / 2
        y = self.__radarHeight / 2
        self.__radar.setTransformOriginPoint(x, y)

        # add self items in items to avoid collisions
        # 添加self.item到items中以防冲突
        self.__items = set([self, self.__base, self.__gun, self.__radar, self.__radarField, self.__largeRadarField,
                            self.__thinRadarField, self.__roundRadarField])

        # 初始化基类
        self.init()

        self.__currentAnimation = []

        # self.a = time.time()

    def advance(self, i):
        """
        if i ==1:
            print(time.time() - self.a)
            self.a = time.time()
        """
        if self.__health <= 0:
            self.gamePlace = len(self.__parent.aliveBots)
            # print("Robot.advance:"+str(self.gamePlace))
            self.__parent.placeList.append(self.__repr__())
            self.__death()

        if self.__currentAnimation == []:
            try:
                self.__currentAnimation = self.__physics.animation.list.pop()

            except IndexError:
                if self.__physics.animation.name == "target":
                    try:
                        self.__physics.animation = self.__runAnimation
                        self.__currentAnimation = self.__physics.animation.list.pop()
                    except IndexError:
                        pass
                else:
                    self.stop()
                    try:
                        self.run()
                    except:
                        traceback.print_exc()
                        exit(-1)
                    self.__physics.reverse()
                    try:
                        self.__currentAnimation = self.__physics.animation.list.pop()
                    except:
                        pass

        if i == 1:
            try:
                command = self.__currentAnimation.pop()  # load animation

                # translation
                dx, dy = self.__getTranslation(command["move"])
                self.setPos(dx, dy)
                # rotation
                angle = self.__getRotation(command["turn"])
                self.__base.setRotation(angle)
                if self.__gunLock.lower() == 'base':
                    self.__gun.setRotation(angle)
                if self.__radarLock.lower() == 'base':
                    self.__setRadarRotation(angle)
                # gun Rotation
                angle = self.__getGunRotation(command["gunTurn"])
                self.__gun.setRotation(angle)
                if self.__radarLock.lower() == 'gun':
                    self.__setRadarRotation(angle)
                # radar Rotation
                angle = self.__getRadarRotation(command["radarTurn"])
                self.__setRadarRotation(angle)
                # asynchronous fire
                if command["fire"] != 0:
                    self.makeBullet(command["fire"])
            except:
                pass

        else:

            self.sensors()

            # collisions
            for item in set(self.__base.collidingItems(1)) - self.__items:
                if isinstance(item, QGraphicsRectItem):
                    # wall Collision
                    self.__wallRebound(item)
                elif isinstance(item, Robot):
                    if item.__base.collidesWithItem(self.__base):
                        # robot Collision
                        self.__robotRebound(item)
                elif isinstance(item, Bullet):
                    # bullet colision
                    self.__bulletRebound(item)
                elif isinstance(item, radarField):
                    if item.robot.__physics.animation.name != "target":
                        # targetSpotted
                        self.__targetSeen(item)

    # -------------------------------------------炮膛-------------------------------------------
    #炮膛转向
    def gunTurn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = int(s * angle / self.__physics.step)
        a = angle % self.__physics.step
        if a != 0:
            self.__physics.gunTurn.append(s * a)
        for i in range(steps):
            self.__physics.gunTurn.append(s * self.__physics.step)

    def lockGun(self, part):
        self.__gunLock = part

    #设置炮膛颜色
    def setGunColor(self, r, g, b):
        color = QColor(r, g, b)
        mask = self.__gun.pixmap.createMaskFromColor(self.gunMaskColor, 1)
        p = QPainter(self.__gun.pixmap)
        p.setPen(QColor(r, g, b))
        p.drawPixmap(self.__gun.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__gun.setPixmap(self.__gun.pixmap)
        self.gunMaskColor = QColor(r, g, b)

    # -------------------------------------------车身（下-------------------------------------
    #车身的移动方式
    def move(self, distance):
        s = 1
        if distance < 0:
            s = -1
        steps = int(s * distance / self.__physics.step)
        d = distance % self.__physics.step
        if d != 0:
            self.__physics.move.append(s * d)
        for i in range(steps):
            self.__physics.move.append(s * self.__physics.step)

    #转向方法，传入的参数为一个角度（类型未知
    def turn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = int(s * angle / self.__physics.step)
        a = angle % self.__physics.step
        if a != 0:
            self.__physics.turn.append(s * a)
        for i in range(steps):
            self.__physics.turn.append(s * self.__physics.step)

    #设置车身颜色
    def setColor(self, r, g, b):
        color = QColor(r, g, b)
        mask = self.__base.pixmap.createMaskFromColor(self.maskColor, 1)
        p = QPainter(self.__base.pixmap)
        p.setPen(QColor(r, g, b))
        p.drawPixmap(self.__base.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__base.setPixmap(self.__base.pixmap)
        self.maskColor = QColor(r, g, b)

    # ---------------------------------------------雷达（下-----------------------------


    def setRadarField(self, form):
        '''
            设置《雷达范围》类型
            类型：normal、large、thin、round
            根据传入的类型来设置显示的类型（其他类型的就hide
        '''
        if form.lower() == "normal":
            self.__radarField.show()
            self.__largeRadarField.hide()
            self.__thinRadarField.hide()
            self.__roundRadarField.hide()
        if form.lower() == "large":
            self.__radarField.hide()
            self.__largeRadarField.show()
            self.__thinRadarField.hide()
            self.__roundRadarField.hide()
        if form.lower() == "thin":
            self.__radarField.hide()
            self.__largeRadarField.hide()
            self.__thinRadarField.show()
            self.__roundRadarField.hide()
        if form.lower() == "round":
            self.__radarField.hide()
            self.__largeRadarField.hide()
            self.__thinRadarField.hide()
            self.__roundRadarField.show()

    def lockRadar(self, part):
        self.__radarLock = part

    #雷达转向
    def radarTurn(self, angle):
        s = 1
        if angle < 0:
            s = -1
        steps = int(s * angle / self.__physics.step)
        a = angle % self.__physics.step
        if a != 0:
            self.__physics.radarTurn.append(s * a)
        for i in range(steps):
            self.__physics.radarTurn.append(s * self.__physics.step)

    #设置雷达颜色（雷达罩的颜色，在坦克车身上的
    def setRadarColor(self, r, g, b):
        color = QColor(r, g, b)
        mask = self.__radar.pixmap.createMaskFromColor(self.radarMaskColor, 1)
        p = QPainter(self.__radar.pixmap)
        p.setPen(QColor(r, g, b))
        p.drawPixmap(self.__radar.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__radar.setPixmap(self.__radar.pixmap)
        self.radarMaskColor = QColor(r, g, b)

    #设置雷达是否可见，将几个雷达类型都设置为统一的
    def radarVisible(self, bol):
        self.__radarField.setVisible(bol)
        self.__roundRadarField.setVisible(bol)
        self.__thinRadarField.setVisible(bol)
        self.__largeRadarField.setVisible(bol)

    # ------------------------------------------------子弹（下------------------------------------

    def fire(self, power):
        # asynchronous fire
        self.stop()
        bullet = Bullet(power, self.bulletColor, self)
        self.__physics.fire.append(bullet)
        self.__items.add(bullet)
        self.__parent.addItem(bullet)
        bullet.hide()
        return id(bullet)

    #制造子弹
    def makeBullet(self, bullet):
        bullet.show()
        pos = self.pos()
        angle = self.__gun.rotation()
        # to find the initial position
        x = pos.x() + self.__baseWidth / 2.0
        y = pos.y() + self.__baseHeight / 2.0
        dx = - math.sin(math.radians(angle)) * self.__gunWidth / 2.0
        dy = math.cos(math.radians(angle)) * self.__gunHeight / 2.0
        pos.setX(x + dx)
        pos.setY(y + dy)
        bot = self
        bullet.init(pos, angle, self.__parent)

        self.__changeHealth(self, -bullet.power)
        return id(bullet)

    #设置子弹颜色
    def setBulletsColor(self, r, g, b):
        self.bulletColor = QColor(r, g, b)

    # ---------------------------------------整体的方法（下---------------------------------------
    def stop(self):
        self.__physics.newAnimation()

    # 获取地图尺寸
    def getMapSize(self):
        return self.__mapSize

    # 获取位置
    def getPosition(self):
        p = self.pos()
        r = self.__base.boundingRect()
        return QPointF(p.x() + r.width() / 2, p.y() + r.height() / 2)

    # 获取炮膛朝向
    def getGunHeading(self):
        angle = self.__gun.rotation()
        # if angle > 360:
        #     a = int(angle) / 360
        #     angle = angle - (360*a)
        return angle

    # 获取朝向
    def getHeading(self):
        return self.__base.rotation()

    # 获取雷达朝向
    def getRadarHeading(self):
        return self.__radar.rotation()

    def reset(self):
        self.__physics.reset()
        self.__currentAnimation = []

    # 获取敌人
    def getEnemiesLeft(self):
        l = []
        for bot in self.__parent.aliveBots:
            dic = {"id": id(bot), "name": bot.__repr__()}
            l.append(dic)
        return l

    # 向细节面板加内容的方法
    def rPrint(self, msg):
        self.info.out.add(str(msg))

    def pause(self, duration):
        self.stop()
        for i in range(int(duration)):
            self.__physics.move.append(0)
        self.stop()

    # -----------------------------------------下面为私有方法------------------------------------------


    def __getTranslation(self, step):
        angle = self.__base.rotation()
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        dx = - math.sin(math.radians(angle)) * step
        dy = math.cos(math.radians(angle)) * step
        # print(dx, dy)
        return x + dx, y + dy

    def __setRadarRotation(self, angle):
        self.__radar.setRotation(angle)
        self.__radarField.setRotation(angle)
        self.__largeRadarField.setRotation(angle)
        self.__thinRadarField.setRotation(angle)

    def __getRotation(self, alpha):
        return self.__base.rotation() + alpha

    def __getGunRotation(self, alpha):
        return self.__gun.rotation() + alpha

    def __getRadarRotation(self, alpha):
        return self.__radar.rotation() + alpha

    def __wallRebound(self, item):
        self.reset()
        if item.name == 'left':
            x = self.__physics.step * 1.1
            y = 0
        elif item.name == 'right':
            x = - self.__physics.step * 1.1
            y = 0
        elif item.name == 'top':
            x = 0
            y = self.__physics.step * 1.1
        elif item.name == 'bottom':
            x = 0
            y = - self.__physics.step * 1.1
        self.setPos(self.pos().x() + x, self.pos().y() + y)
        self.__changeHealth(self, -1)
        self.stop()
        try:
            self.onHitWall()
        except:
            traceback.print_exc()
            exit(-1)
        animation = self.__physics.makeAnimation()
        if animation != []:
            self.__currentAnimation = animation

    def __robotRebound(self, robot):
        try:
            self.reset()
            robot.reset()
            angle = self.__base.rotation()
            pos = self.pos()
            x = pos.x()
            y = pos.y()
            dx = - math.sin(math.radians(angle)) * self.__physics.step * 1.1
            dy = math.cos(math.radians(angle)) * self.__physics.step * 1.1
            self.setPos(x - dx, y - dy)
            pos = robot.pos()
            x = pos.x()
            y = pos.y()
            robot.setPos(x + dx, y + dy)
            self.__changeHealth(robot, -1)
            self.__changeHealth(self, -1)
            self.stop()
            self.onRobotHit(id(robot), robot.__repr__())
            animation = self.__physics.makeAnimation()
            if animation != []:
                self.__currentAnimation = animation
            robot.stop()
            robot.onHitByRobot(id(self), self.__repr__())
            animation = robot.__physics.makeAnimation()
            if animation != []:
                robot.__currentAnimation = animation
        except:
            traceback.print_exc()
            exit(-1)

    def __bulletRebound(self, bullet):
        self.__changeHealth(self, - 3 * bullet.power)
        try:
            if bullet.robot in self.__parent.aliveBots:
                self.__changeHealth(bullet.robot, 2 * bullet.power)
            self.stop()
            self.onHitByBullet(id(bullet.robot), bullet.robot.__repr__(), bullet.power)
            animation = self.__physics.makeAnimation()
            if animation != []:
                self.__currentAnimation = animation
            bullet.robot.stop()
            bullet.robot.onBulletHit(id(self), id(bullet))
            animation = bullet.robot.__physics.makeAnimation()
            if animation != []:
                bullet.robot.__currentAnimation = animation
            self.__parent.removeItem(bullet)
        except:
            pass

    def __targetSeen(self, target):
        self.stop()
        anim = target.robot.__currentAnimation
        target.robot.__physics.animation = target.robot.__targetAnimation
        target.robot.__physics.reset()
        try:
            target.robot.onTargetSpotted(id(self), self.__repr__(), self.getPosition())
        except:
            traceback.print_exc()
            exit(-1)
        target.robot.__physics.newAnimation()
        target.robot.__physics.reverse()
        try:
            target.robot.__currentAnimation = target.robot.__physics.animation.list.pop()
        except:
            target.robot.__physics.animation = target.robot.__runAnimation
            target.robot.__currentAnimation = anim

    def __changeHealth(self, bot, value):
        if bot.__health + value >= 100:
            bot.__health = 100
        else:
            bot.__health = bot.__health + value
        try:
            bot.progressBar.setValue(bot.__health)
        except:
            pass

    def removeMyProtectedItem(self, item):
        self.__items.remove(item)

    def __death(self):

        try:
            self.icon.setIcon(QIcon(os.getcwd() + "/robotImages/dead.png"))
            self.icon2.setIcon(QIcon(os.getcwd() + "/robotImages/dead.png"))
            self.progressBar.setValue(0)
        except:
            pass
        self.__parent.deadBots.append(self)
        self.__parent.aliveBots.remove(self)
        try:
            self.onRobotDeath()
        except:
            traceback.print_exc()
            exit(-1)
        self.__parent.removeItem(self)

        if len(self.__parent.aliveBots) <= 1:  # 如果生存的机器人小于等于1，则结束战斗
            self.__parent.battleFinished()

    def __repr__(self):
        repr = self.__repr.split(".")
        return repr[1].replace("'>", "")
