#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/25/16.
'''


class AnalysixData():
    "数据解析类，用于将发来的数据解析成原本数据"

    def __init__(self, addr, data):
        self.addr = addr
        self.data = data

    def Print(self):
        print(self.data)


class scputimes():
    "cpu信息类，保存cpu相关信息"

    def __init__(self, data):
        "类初始化"
        # data为从客户端发来的数据
        self.data = data
        self.user = data[0]
        self.nice = data[1]
        self.system = data[2]
        self.idle = data[3]
        self.iowait = data[4]
        self.irq = data[5]
        self.softirq = data[6]
        self.steal = data[7]
        self.guest = data[8]
        self.guest_nice = data[9]


class svmem():
    "物理内存类"
    def __init__(self, data):
        "类初始化"
        self.data = data
        self.tatal = data[0]
        self.available = data[1]
        self.percent = data[2]
        self.used = data[3]
        self.free = data[4]
        self.active = data[5]
        self.inactive = data[6]
        self.buffers = data[7]
        self.cached = data[8]
        self.shared = data[9]
class sswap():
   "虚拟内存类"
    def __init__(self,data):
        self.data = data
        self.total = data[0]
        self.used = data[1]
        self.free = data[2]
        self.percent = data[3]
        self.sin = data[4]
        self.sout = data[5]
