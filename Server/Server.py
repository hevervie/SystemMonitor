#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Created by zhoupan on 7/23/16.
"""

import _thread
import threading
from socket import *
from time import ctime

from Configure import Configure
from HandleInfo import InfoCompute


class MainThread(threading.Thread):
    def __init__(self, thread_id, name):
        """一些类初始化工作"""
        threading.Thread.__init__(self)
        threading.threadID = thread_id
        threading.name = name
        cf = Configure()
        self.host = cf.read_config('server.conf', 'server', 'host')
        self.port = int(cf.read_config('server.conf', 'server', 'port'))
        self.max_line = int(cf.read_config('server.conf', 'server', 'max_line'))
        self.buf_size = int(cf.read_config('server.conf', 'buffer', 'size'))
        self.old_data_dict = {}
        self.init_data = (
            (0, 0, 0, 0, 0, 0.0, 0, 0.0, 0.0, 0.0), ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0.0, 0, 0)),
            ((0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0)), {'total': (0, 0, 0, 0, 0, 0, 0, 0)}, (), ())

    def response(self, addr, tcp_client, buf_size):
        """新线程要做的事"""

        print('[ %s ]New process....' % ctime())
        # 接受客户端述数据
        data = tcp_client.recv(buf_size).decode()
        # 将客户端数据转换成列表
        data = tuple(eval(data))

        info = InfoCompute(data, self.old_data_dict[addr])

        print("CPU：%f %%" % info.get_cpu_precent())
        print("memory：%f %%" % info.get_svmem_precent())
        print("swap： %f %%" % info.get_swap_precent())
        print("diskio：%f %%" % info.get_diskio_precent())
        print("diskusage：%f %%" % info.get_diskusage_precent())
        print("netio：%f %%" % info.get_netio_precent())
        print("user：%s" % info.get_user().__str__())
        print("port：%s" % info.get_port().__str__())

        self.old_data_dict[addr] = data

        # 退出后关闭连接
        tcp_client.close()

    def run(self):
        """线程开始后，默认会调用此方法"""
        # 创建一个socket
        tcp_main = socket(AF_INET, SOCK_STREAM)

        # 设置端口可以重用，防止程序一场退出后，马上可以恢复
        tcp_main.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # 绑定地址和端口
        tcp_main.bind((self.host, self.port))
        # 监听连接
        tcp_main.listen(self.max_line)

        while True:
            # print('服务器监听中......')
            tcp_clinet, addr = tcp_main.accept()
            thread1 = threading.Thread()

            # thread1 = ResponseThread(addr, tcp_clinet, self.old_data)
            # thread1.start()

            print('Connect from', addr)

            if addr[0] not in self.old_data_dict.keys():
                self.old_data_dict[addr[0]] = self.init_data

            _thread.start_new_thread(self.response, (addr[0], tcp_clinet, self.buf_size))


# class ResponseThread(threading.Thread):
#     def __init__(self, addr, tcp_clinet, old_data):
#         """作类初始化工作"""
#         threading.Thread.__init__(self)
#         self.addr = addr
#         self.tcp_clinet = tcp_clinet
#         cf = Configure()
#         self.buf_size = int(cf.read_config('server.conf', 'buffer', 'size'))
#         self.old_data = old_data
#
#     def run(self):
#         """线程要做的事"""
#         print('[ %s ]New process....' % ctime())
#         # 接受客户端述数据
#         data = self.tcp_clinet.recv(self.buf_size).decode()
#         # 将客户端数据转换成列表
#         data = tuple(eval(data))
#
#         print(self.old_data)
#         print(self.addr, ":", data)
#
#         info = InfoCompute(data, self.old_data)
#         print(info.get_cpu_precent())
#         self.old_data = data
#         # 退出后关闭连接
#         self.tcp_clinet.close()


if __name__ == '__main__':
    thread = MainThread(1, 'main')
    thread.start()
