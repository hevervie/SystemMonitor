#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Created by zhoupan on 7/23/16.
"""

import _thread
import threading
import simplejson
from socket import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from AlarmModule import Alarm, Strategies
from Configure import Configure
from HandleInfo import InfoCompute, Information
from Persistent import *

# ORM数据库初始化操作
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/test", max_overflow=5)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# 主线程
class MainThread(threading.Thread):
    def __init__(self, thread_id, name):
        """一些类初始化工作"""
        threading.Thread.__init__(self)
        threading.threadID = thread_id
        threading.name = name
        # 读取配置文件
        cf = Configure()
        self.host = cf.read_config('server.conf', 'server', 'host')
        self.port = int(cf.read_config('server.conf', 'server', 'port'))
        self.max_line = int(cf.read_config('server.conf', 'server', 'max_line'))
        self.buf_size = int(cf.read_config('server.conf', 'buffer', 'size'))
        # 保存历史源数据
        self.old_data_dict = {}
        # 保存历史警告数据
        self.old_alarm_dict = {}

        self.init_data = {
            "cpu":
                {"user": 0, "nice": 0, "system": 0, "idle": 0, "iowait": 0, "irq": 0.0,
                 "softirq": 0, "steal": 0.0, "guest": 0.0, "guest_nice": 0.0
                 },

            "mem": {
                "sswap": {"total": 0, "used": 0, "free": 0, "percent": 0.0, "sin": 0, "sout": 0},
                "svmem": {"total": 0, "available": 0, "percent": 0.0, "used": 0, "free": 0, "active": 0,
                          "inactive": 0, "buffers": 0, "cached": 0, "shared": 0
                          }
            },

            "net": {
                "net_avrg": {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 0, "packets_recv": 0, "errin": 0,
                             "errout": 0, "dropin": 0, "dropout": 0},
                "net_count": {
                }
            },

            "user": [{"name": "zhoupan", "terminal": ":0", "host": "localhost", "started": 0.0}
                     ],

            "disk": {
                "disk_io": {"read_count": 0, "write_count": 0, "read_bytes": 0,
                            "write_bytes": 0, "read_time": 0, "write_time": 0,
                            "read_merged_count": 0, "write_merged_count": 0, "busy_time": 0},
                "disk_usage": {"total": 0, "used": 0, "free": 0, "percent": 0}
            },

            "port": []
        }
        self.init_alarm = {
            'cpu': 0,
            'svmem': 0,
            'sswap': 0,
            'disk_io': 0,
            'disk_usage': 0,
            'net_avrg': 0,
            'user': 0,
            'port': 0,
        }

    def response(self, addr, tcp_client, buf_size):
        """新线程要做的事"""

        # 接受客户端述数据
        data = tcp_client.recv(buf_size).decode()
        # 将客户端数据转换成列表

        data = simplejson.loads(data)

        # 对数据进行计算
        info = InfoCompute(data, self.old_data_dict[addr])

        # 获取所有结果
        data_precent = info.return_all_precent()

        # 策略类
        str = Strategies()
        # 获取check的结果
        total, message = str.check_all_data(data_precent, self.old_alarm_dict[addr])

        # 告警
        per = Persistent()
        # 保存所有源数据
        per.save_all_data(data, addr)

        alarm = Alarm()
        # 对数据进行检测，如果超出阈值，则就开始告警
        # sign : 0则表示不进行报警，1则表示告警的级别
        sign = alarm.send_mail(total, message)

        print("%s's sign: %d " % (addr, sign))
        sign = 0
        # 告警过后，将历史数据清空
        if sign:
            total = self.init_alarm
            print("------------------")

        # 将结果保存到列表里面
        data_precent['level'] = sign
        data_precent['message'] = message

        per = Persistent()
        # 保存所有源数据
        per.save_all_data(data, addr)

        # 保存警告后的数据
        per.save_alarm_data(data_precent, addr)
        self.old_alarm_dict[addr] = total
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
        print('服务器监听中......')
        while True:
            # 循环接受客户端的连接
            tcp_clinet, addr = tcp_main.accept()
            # 如果历史数据字典里面没有当前客户段的记录，则就新创建一个，并赋予初始值
            if addr[0] not in self.old_data_dict.keys():
                self.old_data_dict[addr[0]] = self.init_data
                self.old_alarm_dict[addr[0]] = self.init_alarm
            # 创建新的线程，用于处理连接后的后续操作
            _thread.start_new_thread(self.response, (addr[0], tcp_clinet, self.buf_size))


if __name__ == '__main__':
    thread = MainThread(1, 'main')
    thread.start()
