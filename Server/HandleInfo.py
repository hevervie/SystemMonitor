#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 7/25/16.
"""
from mypsutil import scputimes, svmem, sswap, sdiskio, sdiskusage, snetio, suser, port


class Information():
    """数据解析类，用于将发来的数据解析成原本数据"""

    def __init__(self, data):
        self.data = data

    def get_cpu_info(self):
        """获取CPU信息"""
        cpu_info = scputimes(self.data[0])
        return cpu_info

    def get_svmem_info(self):
        """获取物理内存信息"""
        svmem_info = svmem(self.data[1][0])
        return svmem_info

    def get_swap_info(self):
        """获取虚拟内存信息"""
        swap_info = sswap(self.data[1][1])
        return swap_info

    def get_diskio_info(self):
        """获取磁盘IO信息"""
        diskio_info = sdiskio(self.data[2][0])
        return diskio_info

    def get_diskusage_info(self):
        """获取磁盘使用情况"""
        diskusage_info = sdiskusage(self, self.data[2][1])
        return diskusage_info

    def get_netio_info(self):
        """获取网络IO情况"""
        netio_info = []
        for k, v in self.data[3].items():
            net = snetio(k, v)
            netio_info.append(net)
        # 网络IO信息
        netio_info = tuple(netio_info)
        return netio_info

    def get_netio_info_by_name(self, name):
        """通过网口名获取网络信息"""
        total_net = snetio(name, self.data[3][name])
        return total_net

    def get_user_info(self):
        """获取用户登陆情况"""
        user_info = []
        for i in range(len(self.data[4])):
            user = suser(self.data[4][i])
            user_info.append(user)
        # 登陆用户信息
        user_info = tuple(user_info)
        return user_info

    def get_port_info(self):
        """获取端口信息"""
        port_info = port(self.data)
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

        new_total = sum(new_info.get_cpu_info().data)
        old_total = sum(old_info.get_cpu_info().data)

        new_free = new_info.get_cpu_info().idle
        old_free = old_info.get_cpu_info().idle

        cpu_precent = (1 - (new_free - old_free) / (new_total - old_total)) * 100
        cpu_precent = round(cpu_precent, 2)

        return cpu_precent

    def get_svmem_precent(self):
        """获取内存使用率"""
        new_info = Information(self.new_data)
        return new_info.get_svmem_info().precent

    def get_swap_precent(self):
        """获取交换分区使用率"""
        new_info = Information(self.new_data)
        return new_info.get_swap_info().precent

    def get_diskio_precent(self):
        """获取磁盘IO使用率"""
        # new_info = Information(self.new_data)
        # return new_info.get_diskio_info()
        pass

    def get_diskusage_precent(self):
        """获取磁盘使用率"""
        new_info = Information(self.new_data)
        return new_info.get_diskusage_info().precent

    def get_netio_precent(self):
        """获取网络IO使用率"""
        new_info = Information(new_data)
        old_info = Information(old_data)

        new_sent = new_info.get_netio_info_by_name('total').bytes_sent
        old_sent = old_info.get_netio_info_by_name('total').bytes_sent

        new_recv = new_info.get_netio_info_by_name('total').bytes_recv
        old_recv = old_info.get_netio_info_by_name('total').bytes_recv

        netio_precent = ((new_sent - old_sent)+(new_recv - old_recv)*8)/100/1024/1024*10
        return netio_precent

    def get_user(self):
        """获取用户列表"""
        pass

    def get_port(self):
        """获取端口列表"""
        pass


if __name__ == '__main__':
    old_data = "((6033.63, 5.02, 2211.69, 67127.99, 322.92, 0.0, 6.26, 0.0, 0.0, 0.0), ((7584006144, 3362381824, 55.7, 6291951616, 1292054528, 4186767360, 1552982016, 77074432, 1993252864, 548057088), (8589930496, 0, 8589930496, 0.0, 0, 0)), ((81923, 64877, 2200024576, 1875161088, 879576, 4848593, 1872, 46100, 536594), (42123788288, 9685172224, 32438616064, 23.0)), {'lo': (8395, 8395, 59, 59, 0, 0, 0, 0), 'virbr0-nic': (0, 0, 0, 0, 0, 0, 0, 0), 'virbr0': (0, 0, 0, 0, 0, 0, 0, 0), 'total': (17482152, 341779628, 165087, 314725, 0, 0, 0, 0), 'vmnet8': (0, 0, 30, 0, 0, 0, 0, 0), 'vmnet1': (0, 0, 28, 0, 0, 0, 0, 0), 'enp3s0': (17473757, 341771233, 164970, 314666, 0, 0, 0, 0)}, (('zhoupan', ':0', 'localhost', 1469834240.0), ('zhoupan', 'pts/0', 'localhost', 1469834624.0)), ('63342', '80', '8307', '53', '22', '631', '443', '6942', '8000', '902', '3306', '8307', '22', '631', '443', '902'))"
    new_data = "((6139.85, 5.02, 2255.41, 67759.8, 324.04, 0.0, 6.42, 0.0, 0.0, 0.0), ((7584006144, 3344142336, 55.9, 6311165952, 1272840192, 4200693760, 1553850368, 77258752, 1994043392, 548839424), (8589930496, 0, 8589930496, 0.0, 0, 0)), ((81923, 65331, 2200024576, 1887920128, 879576, 4854058, 1872, 46318, 538100), (42123788288, 9685217280, 32438571008, 23.0)), {'vmnet1': (0, 0, 28, 0, 0, 0, 0, 0), 'vmnet8': (0, 0, 30, 0, 0, 0, 0, 0), 'virbr0-nic': (0, 0, 0, 0, 0, 0, 0, 0), 'virbr0': (0, 0, 0, 0, 0, 0, 0, 0), 'total': (17589325, 345702310, 166575, 318002, 0, 0, 0, 0), 'lo': (16259, 16259, 107, 107, 0, 0, 0, 0), 'enp3s0': (17573066, 345686051, 166410, 317895, 0, 0, 0, 0)}, (('zhoupan', ':0', 'localhost', 1469834240.0), ('zhoupan', 'pts/0', 'localhost', 1469834624.0)), ('63342', '80', '8307', '53', '22', '631', '443', '6942', '8000', '902', '3306', '8307', '22', '631', '443', '902'))"
    new_data = tuple(eval(new_data))
    old_data = tuple(eval(old_data))
    info = InfoCompute(new_data, old_data)
    print(info.get_cpu_precent())
    print(info.get_svmem_precent())
    print(info.get_swap_precent())
    print(info.get_netio_precent())

    # ins = Information(new_data)
    # print(ins.get_netio_info_by_name('total').data)
