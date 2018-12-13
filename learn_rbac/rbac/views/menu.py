#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/10 12:34
# @Author  : DollA
# @Theme   : 自动获取权限
from django.conf import settings
from django.utils.module_loading import import_string
from django.shortcuts import HttpResponse

def get_all_urls():
    md = import_string(settings.ROOT_URLCONF)
    
    for item in md.urlpatterns:
        print(item)
        
        
def multi_permission(request):
    get_all_urls()
    
    return HttpResponse('...')