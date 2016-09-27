#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by yangliru,zhoupan on 8/1/16.
"""
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from Configure import Configure


class Alarm():
    def __init__(self):
        """类初始化工作"""
        cf = Configure()
        dict = cf.read_config('strategy.conf', 'mail', 'mail')

        self.server = "smtp.mailgun.org"  # 设置服务器
        self.user = "ru@raydina.me"  # 用户名
        self.passwd = "823264073"  # 口令
        self.mail = eval(dict)  # 告警用户等级字典

    def send_list(self, total):
        match_data = []
        m = max(total)
        level = 0
        for (key, value) in self.mail.items():
            if int(key) <= m:
                for i in value:
                    match_data.append(i)
                if int(key) > level:
                    level = int(key)
        return level, tuple(match_data)

    def send_mail(self, total, ms):
        level, mail_tuple = self.send_list(total)
        # print(mail_tuple)
        # print(ms)
        sign = 0
        for i in range(len(mail_tuple)):
            print(mail_tuple[i])
            print(ms)
            sign = level

        return sign
        # print(mail_tuple[i])
        # message = MIMEText('告警信息:%s' % ms, 'plain', 'utf-8')
        # message['From'] = Header(u"服务器<%s>" % self.user)
        # message['To'] = Header(u"用户 <%s>" % mail_tuple[i])
        # message['Subject'] = Header(u"告警信息")
        # try:
        #     smtpObj = smtplib.SMTP()
        #     smtpObj.connect(self.server, 25)  # 25 为 SMTP 端口号
        #     smtpObj.login(self.user, self.passwd)
        #     smtpObj.sendmail(self.user, mail_tuple[i], message.as_string())
        #     print("邮件发送成功")
        # except smtplib.SMTPException:
        #     print("Error: 无法发送邮件")

        # def send_mail(self, total, ms):
        #     mail_tuple = self.send_list(total)
        #     # print(mail_tuple)
        #     # print(ms)
        #     for i in range(len(mail_tuple)):
        #
        #         # print(mail_tuple[i])
        #         message = MIMEText('告警信息:%s' % ms, 'plain', 'utf-8')
        #         message['From'] = Header(u"服务器<%s>" % self.user)
        #         message['To'] = Header(u"用户 <%s>" % mail_tuple[i])
        #         message['Subject'] = Header(u"告警信息")
        #         try:
        #             smtpObj = smtplib.SMTP()
        #             smtpObj.connect(self.server, 25)  # 25 为 SMTP 端口号
        #             smtpObj.login(self.user, self.passwd)
        #             smtpObj.sendmail(self.user, mail_tuple[i], message.as_string())
        #             print("邮件发送成功")
        #         except smtplib.SMTPException:
        #             print("Error: 无法发送邮件")


class Strategies():
    """告警策略定义"""

    def __init__(self):
        """类初始化"""
        cf = Configure()
        self.cpu_percent = float(cf.read_config('strategy.conf', 'cpu', 'usage'))
        self.svmem_precent = float(cf.read_config('strategy.conf', 'svmem', 'usage'))
        self.swap_precent = float(cf.read_config('strategy.conf', 'swap', 'usage'))
        self.diskio_precent = float(cf.read_config('strategy.conf', 'diskio', 'usage'))
        self.diskusage_precent = float(cf.read_config('strategy.conf', 'diskusage', 'usage'))
        self.netio_precent = float(cf.read_config('strategy.conf', 'netio', 'usage'))
        self.user = tuple(eval(cf.read_config('strategy.conf', 'user', 'user')))
        self.port = tuple(eval(cf.read_config('strategy.conf', 'port', 'port')))

    def check_cpu_data(self, cpu_percent):
        if cpu_percent > self.cpu_percent:
            return 1, "CPU使用率过高"
        else:
            return 0, "CPU使用率正常"

    def check_svmem_data(self, svmem_precent):
        if svmem_precent > self.svmem_precent:
            return 1, "内存使用率过高"
        else:
            return 0, "内存使用率正常"

    def check_swap_data(self, swap_precent):
        if swap_precent > self.swap_precent:
            return 1, "交换分区使用率过高，内存不足"
        else:
            return 0, "交换分区使用率正常"

    def check_diskio_data(self, diskio_precent):
        if diskio_precent > self.diskio_precent:
            return 1, "磁盘IO过高"
        else:
            return 0, "磁盘IO正常"

    def check_diskusage_data(self, diskusage_precent):
        if diskusage_precent > self.diskusage_precent:
            return 2, " 磁盘空间不足"
        else:
            return 0, "磁盘空间充足"

    def check_netio_data(self, netio_precent):
        if netio_precent > self.netio_precent:
            return 1, "网络IO率过高"
        else:
            return 0, "网络IO正常"

    def check_user_data(self, user):
        rtu = "以下用户非法登录："
        sign = 0
        for i in user:
            if i not in self.user:
                rtu += str(i)
                rtu += ','
                sign = 2

        if sign:
            return sign, rtu
        else:
            return 0, "登录用户正常"

    def check_port_data(self, port):
        rtu = "以下端口非法开启："
        sign = 0
        for i in port:
            if i not in self.port:
                rtu += str(i)
                rtu += ','
                sign = 1
        if sign:
            return sign, rtu
        else:
            return 0, "端口开启正常"

    def check_all_data(self, data, old_data):
        """检测所有信息，并返回结果"""

        # 对各项数据进行检测，然后返回结果
        cpu, cpu_message = self.check_cpu_data(data['cpu'])
        svmem, svmem_message = self.check_svmem_data(data['svmem'])
        swap, swap_message = self.check_swap_data(data['sswap'])
        diskio, diskio_message = self.check_diskio_data(data['disk_io'])
        diskusage, diskusage_message = self.check_diskusage_data(data['disk_usage'])
        netio, netio_message = self.check_netio_data(data['net_avrg'])
        user, user_message = self.check_user_data(data['user'])
        port, port_message = self.check_port_data(data['port'])

        # 将所有数据保存下来

        total = {
            'cpu': cpu + old_data['cpu'],
            'svmem': svmem + old_data['svmem'],
            'sswap': swap + old_data['sswap'],
            'disk_io': diskio + old_data['disk_io'],
            'disk_usage': diskusage + old_data['disk_usage'],
            'net_avrg': netio + old_data['net_avrg'],
            'user': user + old_data['user'],
            'port': port + old_data['port']
        }
        message = cpu_message + '\n' + svmem_message + '\n' + swap_message + '\n' + diskio_message + '\n' + diskusage_message + \
                  '\n' + netio_message + '\n' + user_message + '\n' + port_message + '\n'

        return total, message


if __name__ == '__main__':
    # data = (0.0, 39.2, 0.0, 0.0, 24.2, 0.0, ['zhoupan'],
    #         (63342, 80, 8307, 53, 22, 631, 443, 6942, 8000, 902, 3306, 8307, 631, 902))
    # s = Strategies()
    # total, message = s.check_all_data(data)
    # print(total)
    # print(message)
    a = Alarm()
    a.send_mail('zhoupans_mail@163.com', 'hello')
