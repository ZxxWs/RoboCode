from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from Ui_confirmAlert import Ui_ConfirmAlert


class ConfirmAlert(QDialog, Ui_ConfirmAlert):
    ConfirmAlertSignal = QtCore.pyqtSignal(int)  # 用于返回的信号量0是取消、1是确认

    #labelInfor是在label中填充的提示信息
    def __init__(self, labelInfor, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.returnTag = 0
        self.label.setText(labelInfor)
        self.__setUIStyle()

    @pyqtSlot()
    def on_pushButtonOK_clicked(self):
        self.returnTag = 1
        self.close()

    @pyqtSlot()
    def on_pushButtonCancel_clicked(self):
        self.returnTag = 0
        self.close()

    def closeEvent(self, event):
        self.ConfirmAlertSignal.emit(self.returnTag)

    #页面UI的风格设计
    def __setUIStyle(self):

        self.setWindowModality(Qt.ApplicationModal)#设置其他界面不可点击
        self.setFixedSize(self.width(), self.height())  # 固定界面尺寸
        self.setStyleSheet("QLabel{background-color:rgb(255,255,255,0);border-radius: 9px;}"
                           "QLabel{color:#F5FFFA}"
                           "QLabel{font-size:24px;font-family:'楷体'}"
                           "QPushButton{background:rgb(255,255,255,17);border-radius:5px;}"
                           "QPushButton:hover{background:#9AFF9A;color:black}"
                           "QPushButton{font-size:35px;font-family:'楷体'}"
                           "QPushButton{color:#F5FFFA}"
                           "QDialog{background-image:url(ArtResource/backgroudBlack.png)}"
                           "QLineEdit{border-radius:3px}"
                           )
        self.setWindowIcon(QIcon('ArtResource/OK.png'))
        self.pushButtonCancel.setIcon(QIcon("ArtResource/Cancel.png"))
        self.pushButtonOK.setIcon(QIcon("ArtResource/OK.png"))
