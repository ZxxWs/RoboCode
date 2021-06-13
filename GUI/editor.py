import os

from PyQt5.QtCore import pyqtSlot, QTextCodec
from PyQt5.QtWidgets import QDialog, QMessageBox

from GUI.Ui_editor import Ui_Editor


class Editor(QDialog, Ui_Editor):

    def __init__(self, parent, fileName=""):

        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.window = parent
        self.newTag = False  # 用于标志是新建还是修改
        # 新建机器人
        if fileName == "":
            self.newTag = True
            # 将Objects文件夹下的template代码读取后展示（机器人模板
            # print(os.getcwd() + "\\Objects\\template.py")
            with open(os.getcwd() + "\\Objects\\template.py", 'r', encoding='utf-8') as newFile:
                con = newFile.read()
                self.textEdit.setText(con)


        # 打开机器人
        else:
            self.lineEdit.setText(fileName[:-3])
            with open(os.getcwd() + "/Robots/" + fileName, 'r', encoding='utf-8') as openFile:
                con = openFile.read()
                self.textEdit.setText(con)

    @pyqtSlot()
    # 保存文档逻辑
    def on_pushButtonSave_clicked(self):

        inputName = self.lineEdit.text()  # 获取输入的文件名字
        '''如果用户未输入文件名，则系统自动生成一个robot+数字的文件名'''
        if inputName == "":
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请编写文件名。')
            msg_box.exec_()
            return

        # 判断是否重名
        if self.newTag:
            if self.__isRepeat(inputName):
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '文件重名，请修改。')
                msg_box.exec_()
                return
            else:
                self.newTag = False
        # 用于检测文件尾缀是否为.py，如果不是就加个
        if not inputName.endswith('.py'):
            inputName += ".py"

        fileName = r"./Robots/" + inputName
        context = self.textEdit.toPlainText()
        context.encode("UTF-8")

        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(context)
            file.close()

        msg_box = QMessageBox(QMessageBox.Warning, '提醒', '机器人保存成功。')
        msg_box.exec_()
    @pyqtSlot()
    # 关闭编辑界面逻辑
    def on_pushButtonClose_clicked(self):
        self.close()

    def __isRepeat(self, name):

        dirPath = r"./Robots/"
        fileList = os.listdir(dirPath)
        for i in fileList:
            if name == i[:-3]:
                return True
        return False
