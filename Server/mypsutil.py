#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/28/16.
'''
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

    def __init__(self, data):
        "类初始化"
        self.data = data
        self.total = data[0]
        self.used = data[1]
        self.free = data[2]
        self.percent = data[3]
        self.sin = data[4]
        self.sout = data[5]


class sdiskusage():
    "磁盘分区使用率"

    def __init__(self, data):
        "类初始化"
        self.data = data
        self.total = data[0]
        self.used = data[1]
        self.free = data[2]
        self.percent = data[3]


class sdiskio():
    "磁盘IO情况"

    def __init__(self, data):
        "类初始化"
        self.data = data
        self.read_count = data[0]
        self.write_count = data[1]
        self.read_bytes = data[2]
        self.write_bytes = data[3]
        self.read_time = data[4]
        self.write_time = data[5]
        self.read_merged_count = data[6]
        self.write_merged_count = data[7]
        self.busy_time = data[8]


class snetio():
    "网络IO"

    def __init__(self, data, name):
        "类初始化"
        self.name = name
        self.data = data
        self.bytes_sent = data[0]
        self.bytes_recv = data[1]
        self.packets_sent = data[2]
        self.packets_recv = data[3]
        self.errin = data[4]
        self.errout = data[5]
        self.dropin = data[6]
        self.dropout = data[7]


class suser():
    "在线用户信息"

    def __init__(self, data):
        "初始化类"
        self.data = data
        self.name = data[0]
        self.terminal = data[1]
        self.host = data[2]
        self.started = data[3]


class port():
    "端口信息"

    def __init__(self, data):
        "类初始化"
        self.data = data
        self.port = data
