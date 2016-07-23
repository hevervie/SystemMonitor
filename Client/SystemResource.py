#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/22/16.
'''

'''
    依赖包：psutil,subprocess,pip
'''
import psutil
import subprocess

BUF = 1025


class SystemResource():
    "获取系统资源，客户端主类"

    def __init__(self):
        "类创建与初始化工作"
        pass

    def get_cpu_info(self):
        "获取cpu的信息"

        # 获取CPU信息
        cpu_info = psutil.cpu_times(percpu=True)
        return cpu_info

    def get_men_info(self):
        "获取内存信息"

        # 获取内存信息
        virt_mem_info = psutil.virtual_memory()  # 物理内存
        swap_mem_info = psutil.swap_memory()  # 虚拟内存
        return virt_mem_info, swap_mem_info

    def get_disk_info(self,mount_point="/"):
        "获取磁盘占用率和"

        # 获取磁盘信息
        disk_io_count = psutil.disk_io_counters()
        disk_usage = psutil.disk_usage(mount_point)
        return disk_io_count,disk_usage

    def get_net_info(self):
        "获取网络信息"

        # 获取网络信息
        net_io_avrg = psutil.net_io_counters()
        net_io_count = psutil.net_io_counters(pernic=True)
        return net_io_avrg, net_io_count

    def get_user_info(self):
        "获取用户信息"

        # 获取登陆用户信息
        user_info = psutil.users()
        return user_info

    def get_port_info(self):
        "获取主机端口"

        # 获取主机端口
        rtu_code, result = subprocess.getstatusoutput(
            "netstat -tln | awk \'BEGIN{ORS=\",\"}; NR>2{sub(\".*:\", \"\", $4); print $4}\'")
        host_port = result.split(',')
        for i, t in enumerate(host_port):
            if (t == ''):
                host_port.pop(i)
        return host_port


if __name__ == '__main__':
    sr = SystemResource()
    cpu_info = sr.get_cpu_info()
    virt_mem,swap_mem = sr.get_men_info()
    disk_io,disk_usage = sr.get_disk_info()
    net_argv,net_count = sr.get_net_info()
    user_info = sr.get_user_info()
    host_port = sr.get_port_info()

    print("cpu_info:",cpu_info)
    print("virt_mem:",virt_mem)
    print("swap_mem:",swap_mem)
    print("disk_io:",disk_io)
    print("disk_usage:",disk_usage)
    print("net_argv:",net_argv)
    print("net_count:",net_count)
    print("user_info:",user_info)
    print("host_port:",host_port)
