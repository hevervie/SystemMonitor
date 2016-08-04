#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 8/4/16.
"""
import pymysql

conn = pymysql.connect(host='localhost', user='root', passwd='root', db='SysMon', port=3306, charset='utf8')
cur = conn.cursor()
cur.execute('show tables')
d1 = cur.fetchall()
d2 = cur.f
print(d1)
print(d2)
