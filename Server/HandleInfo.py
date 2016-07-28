#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/25/16.
'''
from mypsutil import *

class AnalysixData():
    "数据解析类，用于将发来的数据解析成原本数据"

    def __init__(self, addr, data):
        self.addr = addr
        self.data = data

    def get_cpu_info(self):
        "获取CPU信息"
        cpu_info = scputimes(self.data[0])
        return cpu_info

    def get_svmem_info(self):
        "获取物理内存信息"
        svmem_info = svmem(self.data[1][0])
        return svmem_info

    def get_swap_info(self):
        "获取虚拟内存信息"
        swap_info = sswap(self.data[1][1])
        return swap_info

    def get_diskio_info(self):
        "获取磁盘IO信息"
        diskio_info = sdiskio(self.data[2][0])
        return diskio_info

    def get_diskusage_info(self):
        "获取磁盘使用情况"
        diskusage_info = sdiskusage(self, data[2][1])
        return diskusage_info

    def get_netio_info(self):
        "获取网络IO情况"
        netio_info = []
        for k, v in enumerate(self.data[3]):
            net = snetio(k, v)
            netio_info.append(net)
        # 网络IO信息
        netio_info = tuple(netio_info)
        return netio_info

    def get_user_info(self):
        "获取用户登陆情况"
        user_info = []
        for i in range(len(data[4])):
            user = suser(data[4][i])
            user_info.append(user)
        # 登陆用户信息
        user_info = tuple(user_info)
        return user_info

    def get_port_info(self):
        "获取端口信息"
        port_info = port(data)
        return port_info

    def get_total_info(self):
        total = []
        total.append(self.get_cpu_info())
        total.append(self.get_svmem_info())
        total.append(self.get_swap_info())
        total.append(self.get_diskio_info())
        total.append(self.get_diskusage_info())
        total.append(self.get_netio_info())
        total.append(self.get_user_info())
        total.append(self.get_port_info())
        total = tuple(total)
        return total
    def Print(self):

        print(self.data)
