import os
import pickle
import time

from PyQt5.QtGui import QPixmap

from GUI.Ui_editor import Ui_Editor

'''

filepath= r"Ztest.txt"
con="asdfas.dasdfa.fasd.fafawrgaasdfg"
# with open(filepath,'w') as file:
#     file.write("asasasas")
#     file.close()

pixmap=QPixmap("/robotImages/blast.png")
print(type(pixmap))
'''

# 示例二：
__author__ = 'liaojie'

from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QApplication)


class MainWindow(QGraphicsView):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 创建场景
        self.scene = QGraphicsScene()
        # 在场景中添加文字
        self.scene.addText("Hello, world!")
        # 将场景加载到窗口
        self.setScene(self.scene)


if __name__ == '__main__':
    import sys

    # 每个PyQt程序必须创建一个application对象，sys.argv 参数是命令行中的一组参数
    # 注意：application在 PyQt5.QtWidgets 模块中
    # 注意：application在 PyQt4.QtGui 模块中
    # app = QApplication(sys.argv)
    # 创建桌面窗口
    # mainWindow = MainWindow()
    # 显示桌面窗口
    # mainWindow.show()
    # sys.exit(app.exec_())

    # if os.path.exists(os.getcwd() + "/.datas/lastArena"):  # 获取游戏存档
    #     with open(os.getcwd() + "/.datas/lastArena", 'rb') as file:  # 读取游戏存档
    #
    #         unpickler = pickle.Unpickler(file)
    #         # dico = unpickler.load()
    #         print(file.read())
    #     file.close()

    # 获取当前时间 格式：%Y.%m.%d %H:%M:%S
    print(time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))

    pass








