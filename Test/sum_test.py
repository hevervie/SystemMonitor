#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Created by zhoupan on 8/23/16.
"""
from functools import reduce

list = [1, 2, 3]
r1 = reduce(lambda x, y: x + y, list)
r2 = sum(list)
print(r1)
print(r2)
