import os

from PyQt5.QtCore import pyqtSlot, QTextCodec
from PyQt5.QtWidgets import QDialog

from GUI.Ui_editor import Ui_Editor


class Editor(QDialog, Ui_Editor):

    def __init__(self, parent, fileName=""):

        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.window = parent

        # 新建机器人
        if fileName == "":
            None
        # 打开机器人
        else:
            self.lineEdit.setText(fileName[:-3])
            with open(os.getcwd()+"/Robots/"+fileName, 'r',encoding='GBK') as openFile:
                con = openFile.read()
                self.textEdit.setText(con)


    @pyqtSlot()
    # 保存文档逻辑
    def on_pushButtonSave_clicked(self):

        inputName = self.lineEdit.text()  # 获取输入的文件名字
        '''如果用户未输入文件名，则系统自动生成一个robot+数字的文件名'''
        if inputName == "":
            inputName = "robot"
            dirPath = r"./Robots/"
            fileList = os.listdir(dirPath)
            count = 0
            while 1:
                if inputName + str(count) + ".py" in fileList:
                    count += 1
                else:
                    inputName += str(count)
                    break

        # 用于检测文件尾缀是否为.py，如果不是就加个
        if not inputName.endswith('.py'):
            inputName += ".py"

        fileName = r"./Robots/" + inputName
        context = self.textEdit.toPlainText()

        with open(fileName, 'w',encoding='GBK') as file:
            file.write(context)
            file.close()

    @pyqtSlot()
    # 关闭编辑界面逻辑
    def on_pushButtonClose_clicked(self):
        self.close()
