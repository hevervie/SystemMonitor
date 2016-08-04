#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 8/4/16.
"""


class Persistent():
    """数据持久化类"""

    def __init__(self):
        """类初始化"""
        pass

    def save_all_data(self, data, addr):
        """保存所有的原数据"""

        index = []

        # client 客户端列表
        # 找出客户端是否存在
        sql = "SELECT count(id) FROM client WHERE host = \'%s\';" % addr
        print(sql)
        # 新建新的客户端数据
        sql = "INSERT INTO client(host) VALUES (\'%s\');" % addr
        print(sql)

        # scputimes
        d = data[0]
        sql = "INSERT INTO scputimes(user,nice,system,idle,iowate,irq,softirq,steal,guest,guestnice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
            d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9])
        print(sql)

        # svmem
        d = data[1][0]
        sql = "INSERT INTO svmem(total,available,precent,used,free,active,inactive,buffers,cached,shared) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
            d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9])
        print(sql)

        # sswap
        d = data[1][1]
        sql = "INSERT INTO sswap(total,used,free,precent,sin,sout) VALUES (%s,%s,%s,%s,%s,%s);" % (
            d[0], d[1], d[2], d[3], d[4], d[5])
        print(sql)

        # sdiskio
        d = data[2][0]
        sql = "INSERT INTO sdiskio(read_count,write_count,read_bytes,write_byes,read_time,write_times,read_merged_count,write_merged_count,busy_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
            d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
        print(sql)

        # sdiskusage
        d = data[2][1]
        sql = "INSERT INTO sdiskusage(point,total,used,free,precent) VALUES (\'%s\',%s,%s,%s,%s);" % (
            "/", d[0], d[1], d[2], d[3])
        print(sql)

        # snetio
        d = data[3]
        # 获取type最大值
        sql = "select Max(type) from snetio;"
        type = 0
        print(sql)
        for k, v in d.items():
            sql = "INSERT INTO snetio(device,type,bytes_sent,bytes_recv,package_sent,package_recv,errin,errout,busy_time) VALUES (\'%s\',%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
                k, type, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7])
            print(sql)

        # suser
        d = data[4]
        # 获取type最大值
        sql = "select Max(type) from suser;"
        type = 0
        for v in d:
            sql = "INSERT INTO suser(type,user,terminal,host,started) VALUES (%s,\'%s\',\'%s\',\'%s\',%s);" % (
                type, v[0], v[1], v[2], v[3])
            print(sql)

        # sport
        d = data[5]
        # 获取type最大值
        sql = "select Max(type) from suser;"
        print(sql)
        type = 0
        for v in d:
            sql = "INSERT INTO sport(type,port) VALUES (%s,%s)" % (type, v)
            print(sql)

        # receive
        sql = "INSERT INTO receive(client_id,cpu_id,svmem_id,swap_id,diskio_id,diskusage_id,netio_id,user_id,port_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
            index[0], index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8])

    def save_alarm_data(self, data, addr):
        """保存处理过的告警数据"""

        # 找出客户端
        sql = "SELECT id,count(id) FROM client WHERE host = \'%s\';" % addr
        print(sql)
        index=0
        # 找出数据的id
        sql = "SELECT max(id) FROM receive WHERE client_id = %s " % (index)
        print(sql)


        #
        # sql = "INSERT INTO alarm(client_id,cpu_id,svmem_id,swap_id,diskio_id,diskusage_id,netio_id,user_id,port_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
        #     index[0], index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8])


if __name__ == '__main__':
    data = ((1411.38, 5.03, 390.69, 17315.31, 202.76, 0.0, 2.68, 0.0, 0.0, 0.0), (
        (7584006144, 4612874240, 39.2, 4650770432, 2933235712, 3034529792, 1125998592, 65818624, 1613819904, 193273856),
        (8589930496, 0, 8589930496, 0.0, 0, 0)), (
                (93833, 16742, 2335180288, 534790144, 914777, 3631888, 1828, 12125, 417176),
                (42123788288, 10189336576, 31934451712, 24.2)),
            {'virbr0-nic': (0, 0, 0, 0, 0, 0, 0, 0), 'enp3s0': (5958339, 141404525, 66248, 120225, 0, 0, 0, 0),
             'total': (6702872, 142149058, 70802, 124721, 0, 0, 0, 0), 'vmnet1': (0, 0, 29, 0, 0, 0, 0, 0),
             'lo': (744533, 744533, 4496, 4496, 0, 0, 0, 0), 'virbr0': (0, 0, 0, 0, 0, 0, 0, 0),
             'vmnet8': (0, 0, 29, 0, 0, 0, 0, 0)}, (('zhoupan', ':0', 'localhost', 1470268416.0),), (
                '63342', '80', '8307', '53', '22', '631', '443', '6942', '8000', '902', '3306', '8307', '22', '631',
                '443',
                '902'))
    p = Persistent()
    # p.save_all_data(data, '192.168.30.8')
    p.save_alarm_data(data,'192.168.30.8')
