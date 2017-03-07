#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 3/7/17.
"""
import threadpool
import time
import random


def hello(self):
    time.sleep(2)
    print("test___ %s " % self['1'])
    return "hello"


def thread():
    data = [{'1': 1, '2': 2}]
    requests = threadpool.makeRequests(hello, data)
    [pool.putRequest(req)
     for req in requests]
    pool.wait()


pool = threadpool.ThreadPool(5)
while True:
    print("Test:")
    thread()
