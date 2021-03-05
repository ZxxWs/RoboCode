# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openRobot.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_openRobot(object):
    def setupUi(self, openRobot):
        openRobot.setObjectName("openRobot")
        openRobot.resize(400, 510)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(openRobot)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonOpen = QtWidgets.QPushButton(openRobot)
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.horizontalLayout.addWidget(self.pushButtonOpen)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(openRobot)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(openRobot)
        QtCore.QMetaObject.connectSlotsByName(openRobot)

    def retranslateUi(self, openRobot):
        _translate = QtCore.QCoreApplication.translate
        openRobot.setWindowTitle(_translate("openRobot", "选择打开的机器人"))
        self.pushButtonOpen.setText(_translate("openRobot", "打开"))

