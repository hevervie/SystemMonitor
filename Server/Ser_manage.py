#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/23/16.
'''

import configparser

class ReadConf():
    "读取配置文件"

    def __init__(self):
        "类初始化"
    #def read_conf(self):
        "读取配置文件"

        cf = configparser.ConfigParser()
        cf.read("server.conf")
        self.port = cf.getint("server", "port")
        self.host = cf.get("server", "host")
        self.buf_size = cf.getint("buffer","size")
        self.max_len = cf.getint("server","max_len")

if __name__ == '__main__':
    rc = ReadConf()
   # rc.read_conf()
    print(rc.max_len)
    print(rc.buf_size)
    print(rc.host)
    print(rc.port)