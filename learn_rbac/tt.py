#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/8 23:11
# @Author  : DollA
# @Theme   :

m = ['12','134']
n = []
for i in m:

    while len(i) < 5:
        i = '0'+i
        n.append(i)

print(n)