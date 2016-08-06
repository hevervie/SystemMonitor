#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Created by zhoupan on 7/23/16.
"""

import _thread
import threading
from socket import *

from Alarm import Strategies, Alarm
from Configure import Configure
from HandleInfo import InfoCompute
from Persistent import Persistent


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

        # 接受客户端述数据
        data = tcp_client.recv(buf_size).decode()
        # 将客户端数据转换成列表
        data = tuple(eval(data))

        # 对数据进行计算
        info = InfoCompute(data, self.old_data_dict[addr])
        # 对策略进行check
        str = Strategies()
        # 获取所有结果
        data_precent = info.get_all_precent()
        # 获取check的结果
        total, message = str.check_all_data(data_precent)
        # 告警
        alarm = Alarm()
        # 发送邮件
        alarm.send_mail(total, message)

        data_precent = list(data_precent)
        data_precent.append(total)
        data_precent.append(message)
        per = Persistent()
        # 保存所有源数据
        per.save_all_data(data, addr)
        # 保存警告后的数据
        per.save_alarm_data(data_precent, addr)

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
            if addr[0] not in self.old_data_dict.keys():
                self.old_data_dict[addr[0]] = self.init_data

            _thread.start_new_thread(self.response, (addr[0], tcp_clinet, self.buf_size))


if __name__ == '__main__':
    thread = MainThread(1, 'main')
    thread.start()
