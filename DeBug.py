

class DeBug():
    def debug(indicate,DeBugclass="",DeBugDef=""):
        try:
            print("在"+DeBugclass+"的"+DeBugDef+"中DeBug：",end="")
            print("("+type(indicate)+")",end="")
            print(indicate)
        except:
            print("在" + DeBugclass + "的" + DeBugDef + "中DeBug:输出错误" )