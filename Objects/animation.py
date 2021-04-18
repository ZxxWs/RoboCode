#! /usr/bin/python
#-*- coding: utf-8 -*-

"""
动画类
    属性：自身名称、一个列表
    被physics类调用
"""

class animation():
    
    def __init__(self, name):
        self.list = []
        self.name = name
