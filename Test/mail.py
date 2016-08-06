"""
Mail类：
类名：Mail
功能：解析用户等级，向指定用户列表发送邮件
属性：user dict 告警用户等级字典，id邮箱
方法：
  	方法名：send_list
 		 	形参：level int 报警等级
			返回值：tuple  告警人员邮箱列表
			功能描述：通过报警等级，解析出需要发送的用户邮箱原组，然后返回

	方法名：send_mail
			形参：mail tuple 告警人员邮箱列表
			message string 告警信息
			level int  告警等级
			返回值：Null
	功能描述：给邮件列表发送告警信息
"""

# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import email.utils


class Mail:
    def __init__(self, user_dict, level_int, message_string):
        self.server = "smtp.mailgun.org"  # 设置服务器
        self.user = "ru@raydina.me"  # 用户名
        self.passwd = "823264073"  # 口令
        self.dict = user_dict  # 告警用户等级字典
        self.level = level_int  # 报警等级
        self.info = message_string  # 告警信息

    def send_list(self):
        match_data = []
        for (key, value) in self.dict.items():
            if key <= self.level:
                match_data.append(value)
        return match_data

    def send_mail(self):
        mail_tuple = self.send_list()
        for i in range(len(mail_tuple)):
            print(mail_tuple[i])

            message = MIMEText('告警信息...', 'plain', 'utf-8')
            message['From'] = Header(u"服务器<%s>" % self.user)
            message['To'] = Header(u"用户 <%s>" % mail_tuple[i])
            message['Subject'] = Header(u"告警信息：%s" % self.info)
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(self.server, 25)  # 25 为 SMTP 端口号
                smtpObj.login(self.user, self.passwd)
                smtpObj.sendmail(self.user, mail_tuple[i], message.as_string())
                print("邮件发送成功")
            except smtplib.SMTPException:
                print("Error: 无法发送邮件")


if __name__ == '__main__':
    data = {'1': 'zhoupans_mail@163.com',}
    a = Mail(data, '1', 'warning')
    a.send_mail()
