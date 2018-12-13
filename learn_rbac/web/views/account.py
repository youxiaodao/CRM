#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 15:32
# @Author  : DollA
# @Theme   : 登陆
from django.shortcuts import HttpResponse, render, redirect

from rbac import models
from rbac.service.init_permission import init_permission


def login(request):
    # 1、用户登录
    if request.method == 'GET':
        return render(request, 'login.html')
    # 后期再添加Form或者 ModleForm
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或者密码错误'})
    init_permission(request, current_user)

    return redirect('/customer/list/')


"""
    # 2、权限的初始化，拆分到rbac的service中
    # 根据当前用户获取此用户的所拥有的权限，并放入session中
    # 1、拿到当前用户所有权限的queryset
    permissions_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                   'permissions__url').distinct()

    # 2、获取权限中的url放到列表中，因为session是无法处理queryset
    permissions_list = [item['permissions__url'] for item in permissions_queryset]

    # 3、放入session中
    request.session['permissions_session_key'] = permissions_list
    return redirect('/customer/list/')
"""
