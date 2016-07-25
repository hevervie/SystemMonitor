#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
    Created by zhoupan on 7/25/16.
'''

l=[1,2,3,4]
print(l)
s=l.__str__()
print(type(s))
print(s)

r=list(eval(s))
print(type(r))
print(r)

