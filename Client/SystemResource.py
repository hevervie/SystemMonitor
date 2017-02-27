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

BUF = 1025


class SystemResource():
    """获取系统资源，客户端主类"""

    def __init__(self):
        """类创建与初始化工作"""
        pass

    def get_cpu_info(self, old=None):
        """获取cpu的信息"""

        # 获取CPU信息
        cpu_info = psutil.cpu_times()
        new = {
            'user': cpu_info.user,
            'nice': cpu_info.nice,
            'system': cpu_info.system,
            'idle': cpu_info.idle,
            'iowait': cpu_info.iowait,
            'irq': cpu_info.irq,
            'softirq': cpu_info.softirq,
            'steal': cpu_info.steal,
            'guest': cpu_info.guest,
            'guest_nice': cpu_info.guest_nice
        }
        if old == None:
            return new

        new_total = 0
        old_total = 0

        for k in old:
            if k == 'cpu_percent':
                continue
            old_total += old[k]
        for k in new:
            if k == 'cpu_percent':
                continue
            new_total += new[k]

        new_free = new['idle']
        old_free = old['idle']

        try:
            cpu_percent = (1 - (new_free - old_free) / (new_total - old_total)) * 100
        except ZeroDivisionError:
            new['cpu_percent'] = 0
        else:
            new['cpu_percent'] = cpu_percent
        return new

    def get_men_info(self):
        """获取内存信息"""

        # 获取内存信息
        virt_mem_info = psutil.virtual_memory()  # 物理内存
        swap_mem_info = psutil.swap_memory()  # 虚拟内存

        # 以字典方式返回数据
        mem = {
            'svmem': {
                'total': virt_mem_info.total,
                'available': virt_mem_info.available,
                'percent': virt_mem_info.percent,
                'used': virt_mem_info.used,
                'free': virt_mem_info.free,
                'active': virt_mem_info.active,
                'inactive': virt_mem_info.inactive,
                'buffers': virt_mem_info.buffers,
                'cached': virt_mem_info.cached,
                'shared': virt_mem_info.shared
            },
            'sswap': {
                'total': swap_mem_info.total,
                'used': swap_mem_info.used,
                'free': swap_mem_info.free,
                'percent': swap_mem_info.percent,
                'sin': swap_mem_info.sin,
                'sout': swap_mem_info.sout
            },
        }

        return mem

    def get_disk_info(self, mount_point="/", old=None):
        """获取磁盘占用率和"""

        # 获取磁盘信息
        disk_io_count = psutil.disk_io_counters()
        disk_usage = psutil.disk_usage(mount_point)

        # 以字典方式返回数据
        new = {
            'disk_io': {
                'read_count': disk_io_count.read_count,
                'write_count': disk_io_count.write_count,
                'read_bytes': disk_io_count.read_bytes,
                'write_bytes': disk_io_count.write_bytes,
                'read_time': disk_io_count.read_time,
                'write_time': disk_io_count.write_time,
                'read_merged_count': disk_io_count.read_merged_count,
                'write_merged_count': disk_io_count.write_merged_count,
                'busy_time': disk_io_count.busy_time
            },
            'disk_usage': {
                'total': disk_usage.total,
                'used': disk_usage.used,
                'free': disk_usage.free,
                'percent': disk_usage.percent
            },
        }
        if old == None:
            return new
        new_read = new['disk_io']['read_count']
        old_read = old['disk_io']['read_count']

        new_write = new['disk_io']['write_count']
        old_write = old['disk_io']['write_count']

        new_read_merg = new['disk_io']['read_merged_count']
        old_read_merg = old['disk_io']['read_merged_count']

        new_write_merg = new['disk_io']['write_merged_count']
        old_write_merg = old['disk_io']['write_merged_count']

        try:
            diskio_percent = (new_read_merg - old_read_merg) / (new_read - old_read) + (
                                                                                           new_write_merg - old_write_merg) / (
                                                                                           new_write - old_write)
        except ZeroDivisionError:
            new['disk_io']['diskio_percent'] = 0
        else:
            new['disk_io']['diskio_percent'] = diskio_percent
        return new

    def get_net_info(self, old=None):
        """获取网络信息"""

        # 获取网络信息
        net_io_avrg = psutil.net_io_counters()
        net_io_count = psutil.net_io_counters(pernic=True)
        net_count = {}
        for k in net_io_count:
            net_count[k] = {
                'bytes_sent': net_io_count[k].bytes_sent,
                'bytes_recv': net_io_count[k].bytes_recv,
                'packets_sent': net_io_count[k].packets_sent,
                'packets_recv': net_io_count[k].packets_recv,
                'errin': net_io_count[k].errin,
                'errout': net_io_count[k].errout,
                'dropin': net_io_count[k].dropin,
                'dropout': net_io_count[k].dropout
            }
        # 以字典方式返回数据
        new = {
            'net_avrg': {
                'bytes_sent': net_io_avrg.bytes_sent,
                'bytes_recv': net_io_avrg.bytes_recv,
                'packets_sent': net_io_avrg.packets_sent,
                'packets_recv': net_io_avrg.packets_recv,
                'errin': net_io_avrg.errin,
                'errout': net_io_avrg.errout,
                'dropin': net_io_avrg.dropin,
                'dropout': net_io_avrg.dropout
            },
            'net_count': net_count,
        }

        if old == None:
            return new

        new_sent = new['net_avrg']['bytes_sent']
        old_sent = old['net_avrg']['bytes_sent']

        new_recv = new['net_avrg']['bytes_recv']
        old_recv = old['net_avrg']['bytes_recv']

        try:
            netio_precent = ((new_sent - old_sent) + (new_recv - old_recv) * 8) / 100 / 1024 / 1024 * 10
        except ZeroDivisionError:
            new['net_avrg']['netio_precent'] = 0
        else:
            new['net_avrg']['netio_precent'] = netio_precent

        return new

    def get_user_info(self):
        """获取用户信息"""

        # 获取登陆用户信息
        user_info = psutil.users()
        users = {}
        for i in range(0, len(user_info)):
            users[i] = {
                'name': user_info[i].name,
                'terminal': user_info[i].terminal,
                'host': user_info[i].host,
                'started': user_info[i].started,
            }
        return users

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

    def return_all_info(self, old):
        """返回所有信息"""

        sr = SystemResource()
        data = {
            'cpu': sr.get_cpu_info(old['cpu']),
            'mem': sr.get_men_info(),
            'net': sr.get_net_info(old['net']),
            'disk': sr.get_disk_info(old=old['disk']),
            'user': sr.get_user_info(),
            'port': sr.get_port_info()
        }
        # 返回所有数据
        return data


if __name__ == '__main__':
    sr = SystemResource()
    # print(sr.return_all_info())
    # print(simplejson.loads(sr.return_all_info()))
    # print(sr.get_net_info())
    print(sr.return_all_info().__str__())
