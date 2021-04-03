
import sys
import os
# https://blog.csdn.net/rosefun96/article/details/78909412?ops_request_misc=&request_id=&biz_id=102&utm_term=sys.path.append&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-78909412.first_rank_v2_pc_rank_v29
#sys.path.append():用于添加工作路径，解释见上行链接
#os.getcwd()：获取当前路径
sys.path.append(os.getcwd() + "/GUI")
sys.path.append(os.getcwd() + "/Objects")
sys.path.append(os.getcwd() + "/robotImages")
sys.path.append(os.getcwd() + "/Robots")

from GUI.window import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":

#sys.argv[]是用来获取命令行参数的，sys.argv[0]表示代码本身文件路径;比如在CMD命令行输入 “python test.py -help”，那么sys.argv[0]就代表“test.py”
   app = QApplication(sys.argv)
   app.setApplicationName("Python机器人大战")
   myapp = MainWindow()
   myapp.show()
   sys.exit(app.exec_())


