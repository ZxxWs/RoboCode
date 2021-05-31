import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QHeaderView, QTableWidgetItem

from PyQt5.QtCore import Qt
from GUI.Ui_battleData import Ui_BattleData
from GUI.confirmAlert import ConfirmAlert


class BattleData(QDialog, Ui_BattleData):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.window = parent

        self.__initTable()
        self.__setUIStyle()

    def __initTable(self):

        # 如果项目中不存在存档目录，则创建一个
        if not os.path.exists(os.getcwd() + "/.datas/"):
            os.makedirs(os.getcwd() + "/.datas/")

        self.dataList = os.listdir(os.getcwd() + "/.datas/")
        self.tableWidget.setRowCount(len(self.dataList))

        i = 0
        for data in self.dataList:
            # 向表格中填充按钮

            # itemPath = QTableWidgetItem(self.__dic[listItem])
            itemLable = QTableWidgetItem(data)
            self.tableWidget.setItem(i, 0, itemLable)

            buttonOpen = QPushButton(data)
            buttonDel = QPushButton()

            buttonDel.setIcon(QIcon("ArtResource/del.png"))
            # 按钮逻辑绑定
            # buttonOpen.clicked.connect(self.buttonOpen_clicked)
            buttonDel.clicked.connect(self.buttonDel_clicked)
            # self.tableWidget.setCellWidget(i, 0, buttonOpen)
            self.tableWidget.setCellWidget(i, 1, buttonDel)
            i += 1

        self.tableWidget.setCurrentCell(-1, 0)  # 不加此行时，表格在初始化的时候第一行会被选中（显示高亮


    def buttonDel_clicked(self):

        button = self.sender()
        row = -1
        if button:
            row = self.tableWidget.indexAt(button.pos()).row()

        # 获取删除的行数
        self.__delRow = row

        # 删除弹框--------------------------------------
        tag = "确认删除" + self.dataList[row] + "项目？"
        self.confirmAlert = ConfirmAlert(tag)  # 此处传入的参数1，用于接收返回值
        self.confirmAlert.ConfirmAlertSignal.connect(self.getConfirmAlertSignal)
        self.confirmAlert.show()

    # 获取ConfirmAlert界面返回的信号量
    def getConfirmAlertSignal(self, tag):  # 返回0，表示取消

        if tag == 1:
            self.tableWidget.removeRow(self.__delRow)
            delName = os.getcwd() + "/.datas/" + self.dataList[self.__delRow]

            # 用os库来删除文件
            os.remove(delName)

            # 删除项目文件后，需要修改项目列表
            del self.dataList[self.__delRow]
            # 执行MainWindow的flashPlayData()
            self.window.flashPlayData()

    # 本页面的UI设置
    def __setUIStyle(self):

        # 设置表头格式
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头

        self.setWindowModality(Qt.ApplicationModal)  # 设置其他界面不可点击
        self.setFixedSize(self.width(), self.height())  # 固定界面尺寸
        self.setStyleSheet("QLabel{background-color:rgb(255,255,255,0);border-radius: 9px;font-size:24px}"
                           "QLabel{color:#F5FFFA}"
                           "QLabel{font-size:24px;font-family:'楷体'}"

                           "QPushButton{background:rgb(255,255,255,0);border-radius:5px;}"
                           "QPushButton{font-size:35px;font-family:'楷体'}"
                           "QPushButton:hover{background:#afb4db;}"
                           "QPushButton{text-align:left}"
                           "QPushButton{color:#F5FFFA}"

                           )

        self.tableWidget.setStyleSheet("QTableWidget{background:rgb(100,100,100,0)}"
                                       "QTableWidget{border-style:none}"
                                       "QTableWidget{color:#F5FFFA}"
                                       "QTableWidget{text-align:center}"
                                       "QTableWidget{font-size:35px;font-family:'楷体'}"
                                       )
