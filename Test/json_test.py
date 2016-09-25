#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Created by zhoupan on 9/22/16.
"""
import simplejson
import psutil

data = {
    'name': 'zhoupan',
    'age': 20,
    'score': 91.5
}
cpu = psutil.cpu_times()

print(cpu)

data_json = simplejson.dumps(cpu)
print(data_json)
data_json = simplejson.loads(data_json)
print(data_json)


