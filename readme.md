#  开发问题
1. 关于槽函数绑定问题：  
    python中的槽函数不需要像C++中的显式绑定。而是通过Qt中的@pyqtSlot()函数来实现。[参考链接](https://blog.csdn.net/u010640235/article/details/22149171?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161442593916780255295650%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=161442593916780255295650&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-22149171.first_rank_v2_pc_rank_v29&utm_term=pyqtslot%E7%94%A8%E6%B3%95)  
    例如：按钮名为PushButton,则点击函数写为：   
    >@pyqtSlot()  
    def on_pushButton_clicked(self):  
       
    其中pyqtSlot()中可以带参数。而函数名就为：on_控件名_信号名(self,其他参数)     
   
# 开发事项  
1. 注释：单行注释指的是下边一行代码的作用；或者是本行定义的参数含义。多行注释用于类或者方法，写在类或者方法上面。    


# 开发技术
1. 反射：在GUI.battle.__init__()中用到了反射机制。    
    >官方文档：    
    getattr(object, name[, default])   
    Return the value of the named attribute of object. name must be a string. If the string is the name of one of the object’s attributes, the result is the value of that attribute. For example, getattr(x, 'foobar') is equivalent to x.foobar. If the named attribute does not exist, defaultis returned if provided, otherwise AttributeError is raised.    
   object:对象实例    
   name：(字符串)对象对象的成员函数的名字或者成员变量    
   default：当对象中没有该属性时，返回的默认值    
   异常：当没有该属性并且没有默认的返回值时，抛出"AttrbuteError"     
   
    相当于返回object.name      
    

2. QGraphicsPixmapItem类：[官方文档](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QGraphicsPixmapItem.html)    
3. 自定义的Graph类，继承了QGraphicsScene类：    
    QGraphicsScene 称为图形场景。用于在场景中操作大量的2D图形元素，这个类是作为一个容器QGraphicsItems存在的




V2.1






