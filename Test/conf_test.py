#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
    Created by zhoupan on 8/1/16.
"""
import configparser
from Server.Configure import Configure


cf = configparser.ConfigParser()
cf.read('1.conf')
value = cf.get('user','user')
# print(value)
# print(type(value))
# value=tuple(eval(value))
# print(type(value))
# print(value)
# print(value.__str__())

cf = Configure()
dict = cf.read_config('../Server/strategy.conf', 'mail', 'mail')
print(dict)
print(eval(dict))
print(type(eval(dict)))