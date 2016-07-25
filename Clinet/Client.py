#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/23/16.
'''

import threading
from socket import *
from time import ctime,sleep

from Cli_manage import *
from SystemResource import *

PORT = ReadConf().port
HOST = ReadConf().host
BUFSIZE = ReadConf().buf_size
ADDR = (HOST, PORT)


class Clinet(threading.Thread):
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        threading.threadID = threadID
        threading.name = threadName

    def run(self):
        "线程运行的方法，功能是每隔十秒钟，向服务器发送一下主机信息"

        while True:
            tcpClinet = socket(AF_INET, SOCK_STREAM)
            tcpClinet.connect(ADDR)
            lc = Info_Collect()
            data = lc.data.__str__()
            print(type(data))
            #将列表数据转转换成字符串
            print(data)
            #将数据发送出去
            tcpClinet.send(data.encode())
            #关闭连接
            tcpClinet.close()
            #休眠十秒钟
            sleep(10)


if __name__ == '__main__':
    # "单元测试"
    # lc = Info_Collect()
    # data = lc.data
    # print(len(str(data)))
    # print(lc.data)

    thread = Clinet(1, 'first')
    thread.start()


