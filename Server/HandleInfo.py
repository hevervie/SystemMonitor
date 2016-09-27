#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 7/25/16.
"""


class Information():
    """数据解析类，用于将发来的数据解析成原本数据"""

    def __init__(self, data):
        self.data = data

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

    def select_net_count_info(self):
        """获取网络IO情况"""

        net_count_info = self.data['net']['net_count']
        return net_count_info

    def select_net_avrg_info(self):
        """获取网络IO情况"""

        net_avrg_info = self.data['net']['net_avrg']
        return net_avrg_info

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

    def compute_cpu_precent(self):
        """获取cpu使用率"""

        new_info = Information(self.new_data)
        old_info = Information(self.old_data)

        new_total = 0.0
        old_total = 0.0

        # 计算出cpu各个参数总和

        data = new_info.select_cpu_info()

        for k in data:
            new_total += data[k]
        data = old_info.select_cpu_info()

        for k in data:
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

    def compute_svmem_precent(self):
        """获取内存使用率"""
        new_info = Information(self.new_data)
        return round(new_info.select_svmem_info()['percent'], 2)

    def compute_swap_precent(self):
        """获取交换分区使用率"""
        new_info = Information(self.new_data)
        return round(new_info.select_swap_info()['percent'], 2)

    def compute_diskio_precent(self):
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

    def compute_diskusage_precent(self):
        """获取磁盘使用率"""

        new_info = Information(self.new_data)
        return round(new_info.select_diskusage_info()['percent'], 2)

    def compute_net_avrg_precent(self):
        """获取网络IO使用率"""
        new_info = Information(self.new_data)
        old_info = Information(self.old_data)

        new_sent = new_info.select_net_avrg_info()['bytes_sent']
        old_sent = old_info.select_net_avrg_info()['bytes_sent']

        new_recv = new_info.select_net_avrg_info()['bytes_recv']
        old_recv = old_info.select_net_avrg_info()['bytes_recv']

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
        for item in new_info.select_user_info():
            if item['name'] not in user:
                user.append(item['name'])
        return user

    def get_port(self):
        """获取端口列表"""
        new_info = Information(self.new_data)
        port = new_info.select_port_info()
        return port


if __name__ == '__main__':
    new_data = {
        "cpu": {"user": 1523.03, "nice": 6.29, "system": 3336.07, "idle": 14321.45, "iowait": 451.6, "irq": 0.0,
                "softirq": 35.61, "steal": 0.0, "guest": 0.0, "guest_nice": 0.0}, "mem": {
            "sswap": {"total": 7784624128, "used": 6225920, "free": 7778398208, "percent": 0.1, "sin": 770048,
                      "sout": 6688768},
            "svmem": {"total": 7583969280, "available": 4755673088, "percent": 37.3, "used": 7452553216,
                      "free": 131416064,
                      "active": 4001689600, "inactive": 3065352192, "buffers": 0, "cached": 4624257024,
                      "shared": 3298070528}},
        "net": {

            "net_avrg": {"bytes_sent": 902256173, "bytes_recv": 3148820864, "packets_sent": 2376897,
                         "packets_recv": 2855419, "errin": 0, "errout": 0, "dropin": 0, "dropout": 0},
            "net_count": {
                "virbr0": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 0, "packets_recv": 0, "errin": 0,
                           "errout": 0,
                           "dropin": 0, "dropout": 0},
                "enp3s0": {"bytes_sent": 892814850, "bytes_recv": 3139379541, "packets_sent": 2375416,
                           "packets_recv": 2853964, "errin": 0, "errout": 0, "dropin": 0, "dropout": 0},
                "vmnet8": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 28, "packets_recv": 30, "errin": 0,
                           "errout": 0, "dropin": 0, "dropout": 0},
                "vmnet1": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 28, "packets_recv": 0, "errin": 0,
                           "errout": 0,
                           "dropin": 0, "dropout": 0},
                "virbr0-nic": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 0, "packets_recv": 0, "errin": 0,
                               "errout": 0, "dropin": 0, "dropout": 0},
                "lo": {"bytes_sent": 9441323, "bytes_recv": 9441323, "packets_sent": 1425, "packets_recv": 1425,
                       "errin": 0,
                       "errout": 0, "dropin": 0, "dropout": 0}}},
        "user": [{"name": "zhoupan", "terminal": ":0", "host": "localhost", "started": 1474977920.0}],
        "disk": {
            "disk_io": {"read_count": 305477, "write_count": 133381, "read_bytes": 13048866304,
                        "write_bytes": 9739436032, "read_time": 3072986, "write_time": 16734500,
                        "read_merged_count": 2353, "write_merged_count": 5090, "busy_time": 1036198},
            "disk_usage": {"total": 53660876800, "used": 14018088960, "free": 39642787840, "percent": 26.1}},
        "port": [63342, 80, 8307, 53, 22, 631, 443, 6942, 902, 3306]}
    old_data = {
        "user": [{"name": "zhoupan", "terminal": ":0", "host": "localhost", "started": 1474977920.0}],
        "cpu": {"user": 1447.92, "nice": 6.19, "system": 3192.54, "idle": 13774.97, "iowait": 450.25,
                "irq": 0.0, "softirq": 35.44, "steal": 0.0, "guest": 0.0, "guest_nice": 0.0},
        "mem": {
            "sswap": {"total": 7784624128, "used": 6225920, "free": 7778398208, "percent": 0.1, "sin": 770048,
                      "sout": 6688768},
            "svmem": {"total": 7583969280, "available": 4779831296, "percent": 37.0, "used": 7439413248,
                      "free": 144556032, "active": 3980750848, "inactive": 3076378624, "buffers": 0,
                      "cached": 4635275264, "shared": 3301617664}},
        "port": [63342, 80, 8307, 53, 22, 631, 443, 6942, 902, 3306],

        "net": {
            "net_count": {
                "enp3s0": {"bytes_sent": 892208763, "bytes_recv": 3137862868, "packets_sent": 2373332,
                           "packets_recv": 2851497, "errin": 0, "errout": 0, "dropin": 0, "dropout": 0},
                "lo": {"bytes_sent": 9441323, "bytes_recv": 9441323, "packets_sent": 1425, "packets_recv": 1425,
                       "errin": 0,
                       "errout": 0, "dropin": 0, "dropout": 0},
                "vmnet8": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 28, "packets_recv": 29, "errin": 0,
                           "errout": 0, "dropin": 0, "dropout": 0},
                "vmnet1": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 28, "packets_recv": 0, "errin": 0,
                           "errout": 0,
                           "dropin": 0, "dropout": 0},
                "virbr0-nic": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 0, "packets_recv": 0, "errin": 0,
                               "errout": 0, "dropin": 0, "dropout": 0},
                "virbr0": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 0, "packets_recv": 0, "errin": 0,
                           "errout": 0,
                           "dropin": 0, "dropout": 0}}, "net_avrg": {"bytes_sent": 901650086, "bytes_recv": 3147304191,
                                                                     "packets_sent": 2374813, "packets_recv": 2852951,
                                                                     "errin": 0, "errout": 0, "dropin": 0,
                                                                     "dropout": 0}},
        "disk": {
            "disk_usage": {"total": 53660876800, "used": 14018088960, "free": 39642787840, "percent": 26.1},
            "disk_io": {"read_count": 304907, "write_count": 126004, "read_bytes": 13035374080,
                        "write_bytes": 9604358144, "read_time": 3070008, "write_time": 16401504,
                        "read_merged_count": 2353, "write_merged_count": 4783, "busy_time": 1028825}}}
    info = Information(new_data)
    print("CPU:        ", info.select_cpu_info())
    print("mem:        ", info.select_svmem_info())
    print("swap:       ", info.select_swap_info())
    print("net_count:  ", info.select_net_count_info())
    print("net_avrg:   ", info.select_net_avrg_info())
    print("disk_io:    ", info.select_diskio_info())
    print("disk_usage: ", info.select_diskusage_info())
    print("port:       ", info.select_port_info())
    print("user:       ", info.select_user_info())
    ic = InfoCompute(new_data, old_data)
    print("CPU:        ", ic.compute_cpu_precent())
    print("mem:        ", ic.compute_svmem_precent())
    print("swap:       ", ic.compute_swap_precent())
    print("disk_io:    ", ic.compute_diskio_precent())
    print("disk_usage：", ic.compute_diskusage_precent())
    print("net_avrg:   ", ic.compute_net_avrg_precent())
    print("user:       ", ic.get_user())
    print("port:       ", ic.get_port())
