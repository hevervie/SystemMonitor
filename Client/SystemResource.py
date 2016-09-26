#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 7/22/16.
"""

'''
    依赖包：psutil,subprocess,pip
'''
import subprocess

import psutil
import simplejson

BUF = 1025


class SystemResource():
    """获取系统资源，客户端主类"""

    def __init__(self):
        """类创建与初始化工作"""
        pass

    def get_cpu_info(self):
        """获取cpu的信息"""

        # 获取CPU信息
        cpu_info = psutil.cpu_times()
        return cpu_info

    def get_men_info(self):
        """获取内存信息"""

        # 获取内存信息
        virt_mem_info = psutil.virtual_memory()  # 物理内存
        swap_mem_info = psutil.swap_memory()  # 虚拟内存

        # 以字典方式返回数据
        mem = {
            'svmem': virt_mem_info,
            'sswap': swap_mem_info,
        }

        return mem

    def get_disk_info(self, mount_point="/"):
        """获取磁盘占用率和"""

        # 获取磁盘信息
        disk_io_count = psutil.disk_io_counters()
        disk_usage = psutil.disk_usage(mount_point)

        # 以字典方式返回数据
        disk = {
            'disk_io': disk_io_count,
            'disk_usage': disk_usage,
        }

        return disk

    def get_net_info(self):
        """获取网络信息"""

        # 获取网络信息
        net_io_avrg = psutil.net_io_counters()
        net_io_count = psutil.net_io_counters(pernic=True)

        # 以字典方式返回数据
        net={
            'net_avrg': net_io_avrg,
            'net_count': net_io_count,
        }
        return net

    def get_user_info(self):
        """获取用户信息"""

        # 获取登陆用户信息
        user_info = psutil.users()
        return user_info

    def get_port_info(self):
        """获取主机端口"""
        # 获取主机端口
        rtu_code, result = subprocess.getstatusoutput(
            "netstat -tln | awk \'BEGIN{ORS=\",\"}; NR>2{sub(\".*:\", \"\", $4); print $4}\'")
        host_port = result.split(',')
        port = []
        for i, t in enumerate(host_port):
            if (t == ''):
                host_port.pop(i)
            elif int(t) not in port:
                port.append(int(t))
            else:
                pass
        return port

    def return_all_info(self):
        """返回所有信息"""

        sr = SystemResource()
        data = {
            'cpu': sr.get_cpu_info(),
            'mem': sr.get_men_info(),
            'disk': sr.get_net_info(),
            'net': sr.get_disk_info(),
            'user': sr.get_user_info(),
            'port': sr.get_port_info()
        }

        # 返回所有数据
        return simplejson.dumps(data)


if __name__ == '__main__':
    sr = SystemResource()
    print(sr.return_all_info())
    print(simplejson.loads(sr.return_all_info()))
    print(sr.get_net_info())
