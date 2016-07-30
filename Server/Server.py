#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Created by zhoupan on 7/23/16.
"""

import threading
from socket import *
from time import ctime
from Configure import Configure


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
            thread1 = ResponseThread(addr, tcp_clinet)
            thread1.start()
            #  print('Connect from', addr)


class ResponseThread(threading.Thread):
    def __init__(self, addr, tcp_clinet):
        """作类初始化工作"""
        threading.Thread.__init__(self)
        self.addr = addr
        self.tcp_clinet = tcp_clinet
        cf = Configure()
        self.buf_size = int(cf.read_config('server.conf', 'buffer', 'size'))

    def run(self):
        """线程要做的事"""
        print('[ %s ]New process....' % ctime())
        # 接受客户端述数据
        data = self.tcp_clinet.recv(self.buf_size).decode()
        # 将客户端数据转换成列表
        data = tuple(eval(data))
        print(self.addr, ":", data)
        # 退出后关闭连接
        self.tcp_clinet.close()


if __name__ == '__main__':
    thread = MainThread(1, 'main')
    thread.start()
