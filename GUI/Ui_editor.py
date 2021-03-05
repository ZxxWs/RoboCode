# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editor.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Editor(object):
    def setupUi(self, Editor):
        Editor.setObjectName("Editor")
        Editor.resize(600, 1000)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Editor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonSave = QtWidgets.QPushButton(Editor)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.horizontalLayout.addWidget(self.pushButtonSave)
        self.pushButtonClose = QtWidgets.QPushButton(Editor)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.label = QtWidgets.QLabel(Editor)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Editor)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtWidgets.QTextEdit(Editor)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Editor)
        QtCore.QMetaObject.connectSlotsByName(Editor)

    def retranslateUi(self, Editor):
        _translate = QtCore.QCoreApplication.translate
        Editor.setWindowTitle(_translate("Editor", "Dialog"))
        self.pushButtonSave.setText(_translate("Editor", "保存"))
        self.pushButtonClose.setText(_translate("Editor", "关闭"))
        self.label.setText(_translate("Editor", "文件名："))

