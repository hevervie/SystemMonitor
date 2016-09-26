#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 7/25/16.
"""
from mypsutil import scputimes, svmem, sswap, sdiskio, sdiskusage, snetio, suser, port
import simplejson


class Information():
    """数据解析类，用于将发来的数据解析成原本数据"""

    def __init__(self, data):
        self.data = simplejson.loads(data)

    def select_cpu_info(self):
        """获取CPU信息"""
        cpu_info = self.data['cpu']
        return cpu_info

    def select_svmem_info(self):
        """获取物理内存信息"""
        svmem_info = self.data['mem']['svmem']
        return svmem_info

    def select_swap_info(self):
        """获取虚拟内存信息"""
        swap_info = self.data['mem']['sswap']
        return swap_info

    def select_diskio_info(self):
        """获取磁盘IO信息"""
        diskio_info = self.data['disk']['disk_io']
        return diskio_info

    def select_diskusage_info(self):
        """获取磁盘使用情况"""
        diskusage_info = self.data['disk']['disk_usage']
        return diskusage_info

    def select_netio_info(self):
        """获取网络IO情况"""
        netio_info = self.data['net']['net_count']
        return netio_info

    def select_netio_info_by_name(self, name):
        """通过网口名获取网络信息"""

        total_net = self.data['net']['net_avrg']
        return total_net

    def select_user_info(self):
        """获取用户登陆情况"""

        user_info = self.data['user']
        return user_info

    def select_port_info(self):
        """获取端口信息"""

        port_info = self.data['port']
        return port_info


class InfoCompute():
    """对获取到的信息进行计算，方便进行后续处理"""

    def __init__(self, new_data, old_data):
        """类初始化"""
        self.new_data = new_data
        self.old_data = old_data

    def get_cpu_precent(self):
        """获取cpu使用率"""

        new_info = Information(self.new_data)
        old_info = Information(self.old_data)

        new_total = 0.0
        old_total = 0.0

        # 计算出cpu各个参数总和
        data = new_info.select_cpu_info()
        for k in data.values:
            new_total += data[k]

        data = old_info.select_cpu_info()
        for k in data.values:
            old_total += data[k]

        new_free = new_info.select_cpu_info()['idle']
        old_free = old_info.select_cpu_info()['idle']

        cpu_precent = 0.0

        try:
            cpu_precent = (1 - (new_free - old_free) / (new_total - old_total)) * 100
        except ZeroDivisionError:
            pass
        except Exception:
            pass
        finally:
            return round(cpu_precent, 2)

    def get_svmem_precent(self):
        """获取内存使用率"""
        new_info = Information(self.new_data)
        return round(new_info.select_svmem_info().precent, 2)

    def get_swap_precent(self):
        """获取交换分区使用率"""
        new_info = Information(self.new_data)
        return round(new_info.select_swap_info().precent, 2)

    def get_diskio_precent(self):
        """获取磁盘IO使用率"""
        new_info = Information(self.new_data)
        old_info = Information(self.new_data)

        new_read = new_info.select_diskio_info()['read_count']
        old_read = old_info.select_diskio_info()['read_count']

        new_write = new_info.select_diskio_info()['write_count']
        old_write = old_info.select_diskio_info()['write_count']

        new_read_merg = new_info.select_diskio_info()['read_merged_count']
        old_read_merg = old_info.select_diskio_info()['read_merged_count']

        new_write_merg = new_info.select_diskio_info()['write_merged_count']
        old_write_merg = old_info.select_diskio_info()['write_merged_count']

        diskio_percent = 0.0

        try:
            diskio_percent = (new_read_merg - old_read_merg) / (new_read - old_read) + (
                                                                                           new_write_merg - old_write_merg) / (
                                                                                           new_write - old_write)
        except ZeroDivisionError:
            pass
        except Exception:
            pass
        finally:
            return round(diskio_percent, 2)

    def get_diskusage_precent(self):
        """获取磁盘使用率"""
        new_info = Information(self.new_data)
        return round(new_info.select_diskusage_info()['precent'], 2)

    def get_netio_precent(self):
        """获取网络IO使用率"""
        new_info = Information(self.new_data)
        old_info = Information(self.old_data)

        new_sent = new_info.select_netio_info_by_name('total').bytes_sent
        old_sent = old_info.select_netio_info_by_name('total').bytes_sent

        new_recv = new_info.get_netio_info_by_name('total').bytes_recv
        old_recv = old_info.get_netio_info_by_name('total').bytes_recv
        netio_precent = 0.0
        try:
            netio_precent = ((new_sent - old_sent) + (new_recv - old_recv) * 8) / 100 / 1024 / 1024 * 10
        except ZeroDivisionError:
            pass
        except Exception:
            pass
        finally:
            return round(netio_precent, 2)

    def get_user(self):
        """获取用户列表"""
        new_info = Information(self.new_data)

        user = []
        for i in new_info.get_user_info():
            if i not in user:
                user.append(i.name)
        return tuple(user)

    def get_port(self):
        """获取端口列表"""
        new_info = Information(self.new_data)
        port = new_info.get_port_info().data
        return port

    def get_all_precent(self):
        """获取以上所有信息"""
        data = []
        data.append(self.get_cpu_precent())
        data.append(self.get_svmem_precent())
        data.append(self.get_swap_precent())
        data.append(self.get_diskio_precent())
        data.append(self.get_diskusage_precent())
        data.append(self.get_netio_precent())
        data.append(self.get_user())
        data.append(self.get_port())
        return tuple(data)


if __name__ == '__main__':
    old_data = "((0,0,0, 0, 0, 0.0, 0, 0.0, 0.0, 0.0), ((0,0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0.0, 0, 0)), ((0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0)), {'total': (0, 0, 0, 0, 0, 0, 0, 0)}, (), ())"
    new_data = "((1411.38, 5.03, 390.69, 17315.31, 202.76, 0.0, 2.68, 0.0, 0.0, 0.0), ((7584006144, 4612874240, 39.2, 4650770432, 2933235712, 3034529792, 1125998592, 65818624, 1613819904, 193273856), (8589930496, 0, 8589930496, 0.0, 0, 0)), ((93833, 16742, 2335180288, 534790144, 914777, 3631888, 1828, 12125, 417176), (42123788288, 10189336576, 31934451712, 24.2)), {'virbr0-nic': (0, 0, 0, 0, 0, 0, 0, 0), 'enp3s0': (5958339, 141404525, 66248, 120225, 0, 0, 0, 0), 'total': (6702872, 142149058, 70802, 124721, 0, 0, 0, 0), 'vmnet1': (0, 0, 29, 0, 0, 0, 0, 0), 'lo': (744533, 744533, 4496, 4496, 0, 0, 0, 0), 'virbr0': (0, 0, 0, 0, 0, 0, 0, 0), 'vmnet8': (0, 0, 29, 0, 0, 0, 0, 0)}, (('zhoupan', ':0', 'localhost', 1470268416.0),), ('63342', '80', '8307', '53', '22', '631', '443', '6942', '8000', '902', '3306', '8307', '22', '631', '443', '902'))"
    new_data = tuple(eval(new_data))
    old_data = tuple(eval(old_data))
    info = InfoCompute(new_data, new_data)
    print(info.get_user())
    print(info.get_port())
    print(info.get_diskio_precent())
    print(info.get_diskusage_precent())
    print(info.get_cpu_precent())
    print(info.get_svmem_precent())
    print(info.get_swap_precent())
    print(info.get_netio_precent())
    print(info.get_all_precent())
