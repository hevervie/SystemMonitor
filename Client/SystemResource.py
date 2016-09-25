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
        return virt_mem_info, swap_mem_info

    def get_disk_info(self, mount_point="/"):
        """获取磁盘占用率和"""

        # 获取磁盘信息
        disk_io_count = psutil.disk_io_counters()
        disk_usage = psutil.disk_usage(mount_point)
        return disk_io_count, disk_usage

    def get_net_info(self):
        """获取网络信息"""

        # 获取网络信息
        net_io_avrg = psutil.net_io_counters()
        net_io_count = psutil.net_io_counters(pernic=True)
        return net_io_avrg, net_io_count

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


class Information():
    """信息集和器，将采集的信息集中在一起，方便客户端发送"""

    def __init__(self):
        """类初始化"""
        pass

    def trans_cpu_info(self):
        """转换得到的cpu信息"""
        sr = SystemResource()
        scputimes = sr.get_cpu_info()
        # 将列表转换成原组
        return simplejson.dumps(scputimes)

    def trans_mem_info(self):
        """转换得到的memory信息"""
        sr = SystemResource()
        svmem, sswap = sr.get_men_info()
        # 将列表转换成原组
        mem = {
            'svmem': svmem,
            'sswap': sswap,
        }
        return simplejson.dumps(mem)

    def trans_disk_info(self):
        """转换得到的硬盘信息"""
        sr = SystemResource()
        disk_io, disk_usage = sr.get_disk_info()

        disk_info = {
            'disk_io': disk_io,
            'disk_usage': disk_usage,
        }

        # 将列表转换成原组
        return simplejson.dumps(disk_info)

    def trans_net_info(self):
        """转换得到的网络信息"""

        sr = SystemResource()
        net_argv, net_count = sr.get_net_info()

        net_info = {
            'net_argv': net_argv,
            'net_count': net_count,
        }
        return simplejson.dumps(net_info)

    def trans_user_info(self):
        """转换得到的用户信息"""
        sr = SystemResource()
        user_info = sr.get_user_info()
        return simplejson.dumps(user_info)

    def trans_port_info(self):
        """转换得到的端口信息"""
        sr = SystemResource()
        port = sr.get_port_info()
        port_info = {
            'port': port
        }
        return simplejson.dumps(port_info)

    def return_all_info(self):
        """获取所有信息"""

        info = Information()
        data = {
            'cpu': info.trans_cpu_info(),
            'mem': info.trans_mem_info(),
            'disk': info.trans_disk_info(),
            'net': info.trans_net_info(),
            'user': info.trans_user_info(),
            'port': info.trans_port_info(),
        }
        return simplejson.dumps(data)


if __name__ == '__main__':
    info = Information()
    print(info.trans_user_info())
    print(info.trans_port_info())
    print(info.trans_disk_info())
    print(info.trans_net_info())
    print(info.trans_port_info())
    print(info.return_all_info())
    print(simplejson.loads(info.return_all_info()))
