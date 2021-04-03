import os, pickle

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, QTimer, Qt

from DeBug import DeBug
from GUI.battleData import BattleData
from GUI.openRobot import OpenRobot
from Objects.graph import Graph
from Ui_window import Ui_MainWindow
from battle import Battle
from editor import Editor
from Objects.robot import Robot
from RobotInfo import RobotInfo
from Objects.statistic import statistic

'''
程序最开始的主界面
方法包括几个按钮（以及菜单按钮）
'''


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.countBattle = 0  # 参加战斗的机器人个数
        self.timer = QTimer()  # QTimer是Qt中的一个定时器类，参考文档：https://doc.qt.io/qtforpython-5/PySide2/QtCore/QTimer.html
        self.gameStopTag = False
        # tableWidget是计分面板控件
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 计分板水平表头，设置格式为均匀拉直表头
        self.tableWidget.hide()  # 隐藏计分面板控件
        self.pushButtonGameStop.hide()#暂停游戏按钮隐藏

        # 刷新游戏存档的锁，如果为True，则不会执行on_comboBoxPlayData_currentIndexChanged()
        self.__flashPlayDataTag = False
        self.flashPlayData()

        self.__initUIStyle()

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

        self.pushButtonGameStop.show()#暂停游戏按钮显示


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
        self.sceneMenu = QGraphicsScene()  # sceneMenu为一个qt的场景对象
        self.graphicsView_2.setScene(self.sceneMenu)  # graphicsView_2是UI中的一个graphicsView类型控件，(右侧显示游戏细节信息的控件
        self.scene = Graph(self, self.width, self.height)  # 设置场景的具体宽高
        self.graphicsView.setScene(self.scene)  # 将场景填充到graphicsView控件中
        self.scene.AddRobots(self.botList)  # 此函数属于graph.py中graph类的方法，向战斗场景里添加机器人(图像

        self.timer.timeout.connect(self.scene.advance)
        self.timer.start((self.horizontalSlider.value() ** 2) / 100.0)
        self.resizeEvent()

    @pyqtSlot(int)
    def on_horizontalSlider_valueChanged(self, value):
        self.timer.setInterval((value ** 2) / 100.0)

    @pyqtSlot(str)
    def on_comboBoxPlayData_currentIndexChanged(self, data):

        if self.__flashPlayDataTag:
            return
        if data == "选择记录的战斗":
            return
        else:
            if os.path.exists(os.getcwd() + "/.datas/" + data):  # 获取游戏存档
                with open(os.getcwd() + "/.datas/" + data, 'rb') as file:  # 读取游戏存档
                    unpickler = pickle.Unpickler(file)  # 使用pickle包，读取存档
                    dico = unpickler.load()  # dico是一个字典对象
                file.close()

                # 调用 setUpBattle方法
                self.setUpBattle(dico["width"], dico["height"], dico["botList"])

            else:
                print("No last arena found.")

    @pyqtSlot()
    # 点击新建战斗菜单
    def on_actionNew_triggered(self):

        self.battleMenu = Battle(self)
        self.battleMenu.show()

    @pyqtSlot()
    # 打开战斗记录删除功能
    def on_actionDelete_triggered(self):

        self.battleData = BattleData(self)
        self.battleData.show()

    # 新建机器人按钮
    @pyqtSlot()
    def on_actionNew_2_triggered(self):

        self.Newrobot = Editor(self)
        self.Newrobot.show()

    @pyqtSlot()
    # 打开机器人编辑功能
    def on_actionOpen_triggered(self):

        self.openBot = OpenRobot(self)
        self.openBot.show()

    # 暂停游戏按钮函数
    @pyqtSlot()
    def on_pushButtonGameStop_clicked(self):
        print("执行on_pushButtonGameStop_clicked")
        if not self.gameStopTag:

            self.timer.stop()
            self.pushButtonGameStop.setText("继续游戏")
            self.gameStopTag = True
        else:
            self.timer.start()
            self.pushButtonGameStop.setText("暂停游戏")
            self.gameStopTag = False
        pass

    # ------------------------作用未知，被本类的startBattle方法最后一行调用
    def resizeEvent(self, evt=None):
        try:
            self.graphicsView.fitInView(self.scene.sceneRect(), 4)
        except:
            pass

    # 添加机器人信息，被graph.py中的Graph类的AddRobots()方法调用，
    # 此处的robot参数是./Robots文件下具体的机器人类
    def addRobotInfo(self, robot):
        DeBug.debug(robot, "MainWindow", "addRobotInfo")
        self.sceneMenu.setSceneRect(0, 0, 170, 800)  # 设置机器人细节展示控件的尺寸，左上角是0，0坐标，宽170，高800
        rb = RobotInfo()
        rb.pushButton.setText(str(robot))  # 设置机器人信息UI中的按钮文字
        rb.progressBar.setValue(100)  # 血量条的值
        rb.robot = robot
        robot.info = rb  # 将RobotInfo对象添加到robot信息中
        robot.progressBar = rb.progressBar
        robot.icon = rb.toolButton
        robot.icon2 = rb.toolButton_2
        p = self.sceneMenu.addWidget(rb)  # 将上面设置的机器人信息UI添加到机器人信息场景中
        l = (len(self.scene.aliveBots))  # 获取机器人个数
        self.sceneMenu.setSceneRect(0, 0, 170, l * 80)  # 设置机器人细节展示控件的尺寸，左上角是0，0坐标，这里的l*80是具体的场景尺寸
        p.setPos(0, (l - 1) * 80)  # 设置当前机器人信息UI的位置

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

            self.pushButtonGameStop.setText("暂停游戏")
            self.pushButtonGameStop.hide()  # 暂停游戏按钮隐藏
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

    # 用于刷新战斗记录
    def flashPlayData(self):

        # 如果项目中不存在存档目录，则创建一个
        print("run flashPlayData()")
        self.__flashPlayDataTag = True
        if not os.path.exists(os.getcwd() + "/.datas/"):
            os.makedirs(os.getcwd() + "/.datas/")

        dataList = os.listdir(os.getcwd() + "/.datas/")
        self.comboBoxPlayData.clear()
        self.comboBoxPlayData.addItem("选择记录的战斗")
        self.comboBoxPlayData.addItems(dataList)

        self.__flashPlayDataTag = False

    # 初始化界面的UI风格
    def __initUIStyle(self):

        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet("QMainWindow{background-image:url(ArtResource/backgroudBlack.png)}"
                           "QMainWindow{font-size:35px;font-family:'楷体'}"

                           "QDialog{background-image:url(ArtResource/backgroudBlack.png)}"

                           "QLabel{background-color:rgb(0,0,0,155)}"
                           "QLabel{color:#F5FFFA}"
                           "QLabel{border-radius: 17px}"
                           "QLabel{font-size:35px;font-family:'楷体'}"

                           "QComboBox{border-radius: 4px}"
                           "QComboBox{font-size:35px;font-family:'楷体'}"
                           "QComboBox{text-align:centre}"

                           "QSpinBox{font-size:35px;font-family:'楷体'}"

                           "QPushButton{background:rgb(255,255,255,26);border-radius:5px;}"
                           "QPushButton{font-size:35px;font-family:'楷体'}"
                           "QPushButton:hover{background:green;}"
                           "QPushButton{color:#F5FFFA}"

                           "QTextEdit{font-size:17px;font-family:'楷体'}"
                           
                           "QLineEdit{font-size:17px;font-family:'楷体'}"
                           "QLineEdit{border-radius: 4px}"
                           )
