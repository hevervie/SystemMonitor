#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/23/16.
'''

import configparser
import os


class Configure():
    "读取配置文件"

    def __init__(self):
        "类初始化"
        pass

    def read_config(self, conf_name, section, option):
        "读取配置文件"
        cf = configparser.ConfigParser()
        cf.read(conf_name)
        return cf.getint(section, option)

    def write_config(self, conf_name, section, option, value):
        "写入配置文件"

        #如果指定的文进存在，则以追加方式打开
        if (os.path.exists(conf_name)):

            #以追加方式打开
            fp = open(conf_name, 'a')
            cf = configparser.RawConfigParser()

            #如果section不存在，则需先添加section，再设置值
            if not cf.has_section(section):
                cf.add_section(section)
            #设置值
            cf.set(section, option, value)
        else:

            #以只写方式打开
            fp = open(conf_name, 'w')
            cf = configparser.RawConfigParser()

            #增加section
            cf.add_section(section)
            #设置值
            cf.set(section, option, value)
        #关闭，收尾工作
        cf.write(fp)
        fp.close()


if __name__ == '__main__':
    pass