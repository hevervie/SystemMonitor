#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/22/16.
'''

'''
    依赖包：psutil,subprocess,pip
'''

import psutil
import subprocess

#获取CPU信息
cpu_info=psutil.cpu_times(percpu=True)

#获取内存信息
virt_mem_info=psutil.virtual_memory() #物理内存
swap_mem_info=psutil.swap_memory() #虚拟内存

#获取磁盘信息
disk_io_count=psutil.disk_io_counters() #获取磁盘IO信息
disk_usage=psutil.disk_usage('/') #获取根使用率

#获取网络信息
net_io_avrg=psutil.net_io_counters()
net_io_count=psutil.net_io_counters(pernic=True)

#获取登陆用户信息
user_info=psutil.users()
#获取主机端口
r_code,result=subprocess.getstatusoutput("netstat -tln | awk \'BEGIN{ORS=\",\"}; NR>2{sub(\".*:\", \"\", $4); print $4}\'")
result=result.split(',')

for i,t in enumerate(result):
    if(t==''):
        result.pop(i)


