# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deleteRobot.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_deleteRobot(object):
    def setupUi(self, deleteRobot):
        deleteRobot.setObjectName("deleteRobot")
        deleteRobot.resize(477, 550)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(deleteRobot)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonDelete = QtWidgets.QPushButton(deleteRobot)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.horizontalLayout.addWidget(self.pushButtonDelete)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(deleteRobot)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(deleteRobot)
        QtCore.QMetaObject.connectSlotsByName(deleteRobot)

    def retranslateUi(self, deleteRobot):
        _translate = QtCore.QCoreApplication.translate
        deleteRobot.setWindowTitle(_translate("deleteRobot", "选择删除的机器人"))
        self.pushButtonDelete.setText(_translate("deleteRobot", "删除"))
