#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 7/22/16.
"""

'''
    依赖包：psutil,subprocess,pip
'''
import psutil
import subprocess

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
        scputimes = []
        sr = SystemResource()
        scputimes.append(sr.get_cpu_info().user)
        scputimes.append(sr.get_cpu_info().nice)
        scputimes.append(sr.get_cpu_info().system)
        scputimes.append(sr.get_cpu_info().idle)
        scputimes.append(sr.get_cpu_info().iowait)
        scputimes.append(sr.get_cpu_info().irq)
        scputimes.append(sr.get_cpu_info().softirq)
        scputimes.append(sr.get_cpu_info().steal)
        scputimes.append(sr.get_cpu_info().guest)
        scputimes.append(sr.get_cpu_info().guest_nice)

        # 将列表转换成原组
        return tuple(scputimes)

    def trans_mem_info(self):

        svmem = []
        sswap = []
        sr = SystemResource()
        virt, swap = sr.get_men_info()
        svmem.append(virt.total)
        svmem.append(virt.available)
        svmem.append(virt.percent)
        svmem.append(virt.used)
        svmem.append(virt.free)
        svmem.append(virt.active)
        svmem.append(virt.inactive)
        svmem.append(virt.buffers)
        svmem.append(virt.cached)
        svmem.append(virt.shared)

        sswap.append(swap.total)
        sswap.append(swap.used)
        sswap.append(swap.free)
        sswap.append(swap.percent)
        sswap.append(swap.sin)
        sswap.append(swap.sout)

        # 将列表转换成原组
        return tuple(svmem), tuple(sswap)

    def trans_disk_info(self):
        sr = SystemResource()
        disk_io, disk_usage = sr.get_disk_info()

        sdiskio = []
        sdiskusage = []

        sdiskio.append(disk_io.read_count)
        sdiskio.append(disk_io.write_count)
        sdiskio.append(disk_io.read_bytes)
        sdiskio.append(disk_io.write_bytes)
        sdiskio.append(disk_io.read_time)
        sdiskio.append(disk_io.write_time)
        sdiskio.append(disk_io.read_merged_count)
        sdiskio.append(disk_io.write_merged_count)
        sdiskio.append(disk_io.busy_time)

        sdiskusage.append(disk_usage.total)
        sdiskusage.append(disk_usage.used)
        sdiskusage.append(disk_usage.free)
        sdiskusage.append(disk_usage.percent)

        # 将列表转换成原组
        return tuple(sdiskio), tuple(sdiskusage)

    def trans_net_info(self):
        sr = SystemResource()
        net_argv, net_count = sr.get_net_info()
        snetio = {}
        total = []

        total.append(net_argv.bytes_sent)
        total.append(net_argv.bytes_recv)
        total.append(net_argv.packets_sent)
        total.append(net_argv.packets_recv)
        total.append(net_argv.errin)
        total.append(net_argv.errout)
        total.append(net_argv.dropin)
        total.append(net_argv.dropout)
        snetio['total'] = tuple(total)
        for k, v in net_count.items():
            tmp = []
            tmp.append(v.bytes_sent)
            tmp.append(v.bytes_recv)
            tmp.append(v.packets_sent)
            tmp.append(v.packets_recv)
            tmp.append(v.errin)
            tmp.append(v.errout)
            tmp.append(v.dropin)
            tmp.append(v.dropout)

            # 列表转原组
            snetio[k] = tuple(tmp)

        # 字典不可转为原组，忽略
        return snetio

    def trans_user_info(self):
        sr = SystemResource()
        user_info = sr.get_user_info()
        suser = []
        for i in range(0, len(user_info), 1):
            tmp = []
            tmp.append(user_info[i].name)
            tmp.append(user_info[i].terminal)
            tmp.append(user_info[i].host)
            tmp.append(user_info[i].started)

            suser.append(tuple(tmp))
        return tuple(suser)

    def trans_port_info(self):
        sr = SystemResource()
        port = sr.get_port_info()
        return tuple(port)

    def trans_all_info(self):
        data = []
        info = Information()
        data.append(info.trans_cpu_info())
        data.append(info.trans_mem_info())
        data.append(info.trans_disk_info())
        data.append(info.trans_net_info())
        data.append(info.trans_user_info())
        data.append(info.trans_port_info())
        return tuple(data)


if __name__ == '__main__':
    info = Information()
    print(info.trans_all_info())
