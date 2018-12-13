#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/9 11:38
# @Author  : DollA
# @Theme   :
from django.shortcuts import render
from rbac import models


def role_list(request):
    """
    
    :param request: 
    :return: 
    """
    role_queryset = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'role_list': role_queryset})
