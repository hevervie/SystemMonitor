#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/25/16.
'''


class AnalysixData():
    "数据解析类，用于将发来的数据解析成原本数据"

    def __init__(self, addr, data):
        self.addr = addr
        self.data = data

    def Print(self):
        print(self.data)

