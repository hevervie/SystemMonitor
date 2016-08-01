#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by yangliru on 8/1/16.
"""
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class Alam():
    def __init__(self, mail, level, message):
        self.server = "smtp.mailgun.org"  # 设置服务器
        self.user = "ru@raydina.me"  # 用户名
        self.passwd = "823264073"  # 口令
        self.mail = mail  # 告警用户等级字典
        self.level = level  # 报警等级
        self.message = message  # 告警信息

    def send_list(self):
        match_data = []
        for (key, value) in self.mail.items():
            if int(key) <= self.level:
                match_data.append(value)
        return match_data

    def send_mail(self):
        mail_tuple = self.send_list()
        for i in range(len(mail_tuple)):
            print(mail_tuple[i])
            message = MIMEText('告警信息:%s' % self.message , 'plain', 'utf-8')
            message['From'] = Header(u"服务器<%s>" % self.user)
            message['To'] = Header(u"用户 <%s>" % mail_tuple[i])
            message['Subject'] = Header(u"告警信息")
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(self.server, 25)  # 25 为 SMTP 端口号
                smtpObj.login(self.user, self.passwd)
                smtpObj.sendmail(self.user, mail_tuple[i], message.as_string())
                print("邮件发送成功")
            except smtplib.SMTPException:
                print("Error: 无法发送邮件")


if __name__ == '__main__':
    data = {'1': 'zhoupans_mail@163.com', '2': 'zhoupan@xiyoulinux.org'}
    a = Alam(data, 2, '一号机器CPU使用率过高！')
    a.send_mail()
