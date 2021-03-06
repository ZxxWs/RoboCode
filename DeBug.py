'''
自定义的测试类

'''


class DeBug():
    def debug(indicate, DeBugclass="", DeBugDef=""):
        try:
            print("在" + DeBugclass + "的" + DeBugDef + "中DeBug：", end="")
            print(type(indicate), end="-->")
            print(indicate)
        except:
            print("在" + DeBugclass + "的" + DeBugDef + "中DeBug:输出错误")

    def debugobj(indicate, obj, DeBugDef=""):
        try:
            print("在" + type(obj) + "的" + DeBugDef + "中DeBug：", end="")
            print(type(indicate), end="-->")
            print(indicate)
        except:
            print("在" + type(obj) + "的" + DeBugDef + "中DeBug:输出错误")
