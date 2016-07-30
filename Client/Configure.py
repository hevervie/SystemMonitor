#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 7/23/16.
"""
import configparser


class Configure():
    """
        读取配置文件
    """

    def __init__(self):
        """类初始化"""
        pass

    def read_config(self, conf_name, section, option):
        """读取配置文件"""
        value = ""
        try:
            cf = configparser.ConfigParser()
            cf.read(conf_name)
            value = cf.get(section, option)
        except Exception:
            pass
        finally:
            return value

    def write_config(self, conf_name, value):
        """写入配置文件"""

        # 打开文件
        fp = open(conf_name, 'w')
        cf = configparser.ConfigParser()
        # 遍历字典，并写入文件
        for (k, v) in value.items():
            cf.add_section(str(k))
            for (e, a) in v.items():
                cf.set(str(k), str(e), str(a))
        cf.write(fp)
        fp.close()


if __name__ == '__main__':
    c = Configure()
  #  print(c.write_config('1.conf', {'client': {}, 'server': {'port': 8000, 'host': '192.168.30.2'}}))
    print(c.read_config('client.conf', 'server', 'port'))
