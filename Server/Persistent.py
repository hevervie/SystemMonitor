#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 8/4/16.
"""
# 导入mysql的包
import pymysql
from Configure import Configure
import datetime
from SQL.Models import Scputimes, Svmem, Sswap, Sdiskio, Sdiskusage, Snetio, Suser, Sport, Client, Receive, Alarm, \
    Strategy, User, Port

from Server import session
from sqlalchemy import func


class Persistent():
    """数据持久化类"""

    def __init__(self):
        """类初始化"""
        cf = Configure()
        self.host = cf.read_config('server.conf', 'mysql', 'host')
        self.port = int(cf.read_config('server.conf', 'mysql', 'port'))
        self.db = cf.read_config('server.conf', 'mysql', 'database')
        self.user = cf.read_config('server.conf', 'mysql', 'user')
        self.passwd = cf.read_config('server.conf', 'mysql', 'passwd')

    def save_all_data(self, data, addr):
        """保存所有的原数据"""
        index = {}
        # conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port,
        #                        charset='utf8')
        # cur = conn.cursor()

        # # client 客户端列表
        # # 找出客户端是否存在
        # sql = "SELECT count(id),id FROM informations_client WHERE host = \'%s\';" % addr
        # # 执行sql语句
        # cur.execute(sql)
        # # 获取结果
        # result = cur.fetchall()

        # ORM替代方案
        result = session.query(Client).filter_by(name=addr).all()

        # # 如果此客户端不存在
        # if result[0][0] == 0:
        #     # 新建新的客户端数据
        #     sql = "INSERT INTO informations_client(host) VALUES (\'%s\');" % addr
        #     cur.execute(sql)
        #     # 将运行结果提交
        #     index['client_id'] = conn.insert_id()
        #     conn.commit()
        # # 如果存在，则将此id记录下来
        # else:
        #     index['client_id'] = result[0][1]
        #
        # d = data['cpu']
        # sql = "INSERT INTO informations_scputimes(user,nice,system,idle,iowait,irq,softirq,steal,guest,guest_nice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
        #     d['user'], d['nice'], d['system'], d['idle'], d['iowait'], d['irq'], d['softirq'], d['steal'], d['guest'],
        #     d['guest_nice'])
        # cur.execute(sql)
        # index['cpu_id'] = conn.insert_id()
        # conn.commit()

        # ORM替代方案
        if result.count() == 0:
            client = Client(host=addr)
            session.add(client)
            session.commit()
            index['client_id'] = client.id
        else:
            index['client_id'] = result[0].id
        d = data['cpu']
        scputimes = Scputimes(user=d['user'], nice=d['nice'], system=d['system'], idle=d['idle'], iowait=d['iowait'],
                              irq=d['irq'], softirq=d['softirq'], steal=d['steal'], guest=d['guest'],
                              guest_nice=d['guest_nice'])
        session.add(scputimes)
        session.commit()
        index['cpu_id'] = scputimes.id

        # # svmem
        # d = data['mem']['svmem']
        # sql = "INSERT INTO informations_svmem(total,available,percent,used,free,active,inactive,buffers,cached,shared) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
        #     d['total'], d['available'], d['percent'], d['used'], d['free'], d['active'], d['inactive'], d['buffers'],
        #     d['cached'], d['shared'])
        # cur.execute(sql)
        # index['svmem_id'] = conn.insert_id()
        # conn.commit()

        # svmem
        d = data['mem']['svmem']
        svmem = Svmem(total=d['total'], available=d['available'], percent=d['percent'], used=d['used'], free=d['free'],
                      active=d['active'], inactive=d['inactive'], buffers=d['buffers'], cached=d['cached'],
                      shared=d['shared'])
        session.add(svmem)
        session.commit()
        index['svmem_id'] = svmem.id

        # # sswap
        # d = data['mem']['sswap']
        # sql = "INSERT INTO informations_sswap(total,used,free,percent,sin,sout) VALUES (%s,%s,%s,%s,%s,%s);" % (
        #     d['total'], d['used'], d['free'], d['percent'], d['sin'], d['sout'])
        # cur.execute(sql)
        # index['sswap_id'] = conn.insert_id()
        # conn.commit()

        # sswap
        d = data['mem']['sswap']
        sswap = Sswap(total=d['total'], used=d['used'], free=d['free'], percent=d['percent'], sin=d['sin'],
                      sout=d['sout'])
        session.add(sswap)
        session.commit()
        index['sswap_id'] = sswap.id

        # # sdiskio
        # d = data['disk']['disk_io']
        # sql = "INSERT INTO informations_sdiskio(read_count,write_count,read_bytes,write_bytes,read_time,write_time,read_merged_count,write_merged_count,busy_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
        #     d['read_count'], d['write_count'], d['read_bytes'], d['write_bytes'], d['read_time'], d['write_time'],
        #     d['read_merged_count'], d['write_merged_count'], d['busy_time'])
        # cur.execute(sql)
        # index['diskio_id'] = conn.insert_id()
        # conn.commit()

        # sdiskio
        d = data['disk']['disk_io']
        sdiskio = Sdiskio(read_count=d['read_count'], write_count=d['write_count'], read_bytes=d['read_bytes'],
                          write_bytes=d['write_bytes'], read_time=d['read_time'], write_time=d['write_time'],
                          read_merged_count=d['read_merged_count'], write_merged_count=d['write_merged_count'],
                          busy_time=d['busy_time'])
        session.add(sdiskio)
        session.commit()
        index['diskio_id'] = sdiskio.id

        # # sdiskusage
        # d = data['disk']['disk_usage']
        # sql = "INSERT INTO informations_sdiskusage(point,total,used,free,percent) VALUES (\'%s\',%s,%s,%s,%s);" % (
        #     "/", d['total'], d['used'], d['free'], d['percent'])
        # cur.execute(sql)
        # index['diskusage_id'] = conn.insert_id()
        # conn.commit()

        # sdiskusage
        d = data['disk']['disk_usage']
        sdiskusage = Sdiskusage(point=d['point'], total=d['total'], used=d['used'], free=d['free'],
                                percent=d['percent'])
        session.add(sdiskusage)
        session.commit()
        index['diskusage_id'] = sdiskusage

        # # snetio
        # # 获取type最大值
        # sql = "select Max(type) from informations_snetio;"
        # cur.execute(sql)
        # result = cur.fetchall()
        # type = 0
        # if result[0][0] == None or result[0][0] == 0:
        #     type = 1
        # else:
        #     type = result[0][0] + 1
        #
        # d = data['net']['net_avrg']
        # sql = "INSERT INTO informations_snetio(device,type,bytes_sent,bytes_recv,packets_sent,packets_sent,errin,errout,dropin,dropout) VALUES (\'%s\',%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
        #     "net_avrg", type, d['bytes_sent'], d['bytes_recv'], d['packets_sent'], d['packets_recv'], d['errin'],
        #     d['errout'], d['dropin'], d['dropout'])
        # cur.execute(sql)
        # conn.commit()

        # d = data['net']['net_count']
        # for k, v in d.items():
        #     sql = "INSERT INTO informations_snetio(device,type,bytes_sent,bytes_recv,packets_sent,packets_recv,errin,errout,dropin,dropout) VALUES (\'%s\',%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (
        #         k, type, v['bytes_sent'], v['bytes_recv'], v['packets_sent'], v['packets_recv'], v['errin'],
        #         v['errout'], v['dropin'], v['dropout'])
        #     cur.execute(sql)
        #     conn.commit()
        #
        # index['netio_type'] = type

        # snetio
        result = session.query(func.max(Snetio.type))
        type = result[0][0]
        if type == None:
            type = 1
        else:
            type += 1
        d = data['net']['net_avrg']
        snetio = Snetio(device='net_avrg', type=type, bytes_sent=d['bytes_sent'], bytes_recv=d['bytes_recv'],
                        packets_sent=d['packets_sent'], packets_recv=d['packets_recv'], errin=d['errin'],
                        errout=d['errout'], dropin=d['dropin'], dropout=d['dropout'])
        session.add(snetio)
        session.commit()

        d = data['net']['net_count']
        for k, v in d.items():
            snetio = Snetio(device=k, type=type, bytes_sent=v['bytes_sent'], bytes_recv=v['bytes_recv'],
                            packets_sent=v['packets_sent'], packets_recv=v['packets_recv'], errin=v['errin'],
                            errout=v['errout'], dropin=v['dropin'], dropout=v['dropout'])
            session.add(snetio)
        session.commit()
        index['netio_type'] = type

        # # suser
        # # 获取type最大值
        # sql = "select Max(type) from informations_suser;"
        # cur.execute(sql)
        # result = cur.fetchall()
        # type = 0
        # if result[0][0] == None or result[0][0] == 0:
        #     type = 1
        # else:
        #     type = result[0][0] + 1
        #
        # d = data['user']
        # for v in d:
        #     sql = "INSERT INTO informations_suser(type,name,terminal,host,started) VALUES (%s,\'%s\',\'%s\',\'%s\',%s);" % (
        #         type, v['name'], v['terminal'], v['host'], v['started'])
        #     cur.execute(sql)
        #     conn.commit()
        # index['user_type'] = type

        # suser
        result = session.query(func.max(Suser.type))
        type = result[0][0]
        if type == None:
            type = 1
        else:
            type += 1

        d = data['user']
        for v in d:
            suser = Suser(type=type, name=v['name'], terminal=v['terminal'], host=v['host'], started=v['started'])
            session.add(suser)
        session.commit()
        index['user_type'] = type

        # # sport
        # d = data['port']
        # # 获取type最大值
        # sql = "select Max(type) from informations_sport;"
        # type = 0
        # cur.execute(sql)
        # result = cur.fetchall()
        # if result[0][0] == None or result[0][0] == 0:
        #     type = 1
        # else:
        #     type = result[0][0] + 1
        # for v in d:
        #     sql = "INSERT INTO informations_sport(type,port) VALUES (%s,%s)" % (type, v)
        #     cur.execute(sql)
        #     conn.commit()
        # index['port_type'] = type

        # sport
        d = data['port']
        result = session.query(func.max(Sport.type))
        type = result[0][0]
        if type == None:
            type = 1
        else:
            type += 1
        for v in d:
            suser = Sport(type=type, port=v)
            session.add(suser)
        session.commit()
        index['port_type'] = type

        # # receive
        # sql = "INSERT INTO informations_receive(client_id,cpu_id,svmem_id,sswap_id,diskio_id,diskusage_id,netio_type,user_type,port_type,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,\'%s\')" % (
        #     index['client_id'], index['cpu_id'], index['svmem_id'], index['sswap_id'], index['diskio_id'],
        #     index['diskusage_id'], index['netio_type'], index['user_type'], index['port_type'],
        #     datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
        # print(sql)
        # cur.execute(sql)
        # conn.commit()
        # conn.close()

        # receive
        now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        receive = Receive(client_id=index['client_id'], cpu_id=index['cpu_id'], svmem_id=index['svmem_id'],
                          sswap_id=index['sswap_id'], diskio_id=index['diskio_id'], diskusage_id=index['diskusage_id'],
                          netio_type=index['netio_type'], user_type=index['user_type'], port_type=index['port_type'],
                          datetime=now)
        session.add(receive)
        session.commit()

    def save_alarm_data(self, data, addr):
        """保存处理过的告警数据"""

        # # 连接数据库
        # conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port,
        #                        charset='utf8')
        # # 获取游标
        # cur = conn.cursor()
        # # 找出客户端
        # sql = "SELECT count(id),id FROM informations_client WHERE host = \'%s\';" % addr
        # cur.execute(sql)
        # result = cur.fetchall()
        # if result[0][0] == 0:
        #     # 新建新的客户端数据
        #     sql = "INSERT INTO informations_client(host) VALUES (\'%s\');" % addr
        #     cur.execute(sql)
        #     # 将运行结果提交
        #     conn.commit()
        # else:
        #     index = result[0][1]
        #     # 找出数据的id
        #     sql = "SELECT max(id),id FROM informations_receive WHERE client_id = %s " % (index)
        #     cur.execute(sql)
        #     result = cur.fetchall()
        #     if result[0][0] == None or result[0][0] == 0:
        #         pass
        #     else:
        #         recv = result[0][0]
        #         sql = "INSERT INTO informations_alarm(recv_id,client_id,cpu,svmem,swap,diskio,diskusage,snetio,level,message) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,\'%s\')" % (
        #             recv, index, data['cpu'], data['svmem'], data['sswap'], data['disk_io'], data['disk_usage'],
        #             data['net_avrg'], data['level'], data['message'])
        #         cur.execute(sql)
        #         # 将运行结果提交
        #         conn.commit()
        result = session.query(Client).filter_by(name=addr).all()
        if result.count() <= 0:
            client = Client(host=addr)
            session.add(client)
            session.commit()
        else:
            index = result[0].id
            result = session.query(func.max(Receive.id)).filter_by(client_id=index)
            recv = result[0][0]
            if recv is None:
                pass
            else:
                alarm = Alarm(recv_id=recv, client_id=index, cpu=data['cpu'], svmem=data['svmem'], swap=data['swap'],
                              diskio=data['diskio'], diskusage=data['diskusage'], snetio=data['snetio'],
                              level=data['level'], message=data['message'])
                session.add(alarm)
                session.commit()


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
                '443', '902'))
    p = Persistent()
    p.save_alarm_data(data, '192.168.30.8')
