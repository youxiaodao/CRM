#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 17:44
# @Author  : DollA
# @Theme   : 权限的初始化
from django.conf import settings


def init_permission(request, current_user):
    """
    用户权限的初始化
    :param request: 请求相关数据
    :param current_user: 当前用户数据
    :return:
    """
    # 根据当前用户获取此用户的所拥有的权限，并放入session中
    # 1、拿到当前用户所有权限的queryset
    permissions_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                       'permissions__url',
                                                                                       'permissions__title',
                                                                                       'permissions__pid',
                                                                                       'permissions__name',
                                                                                       'permissions__pid__title',
                                                                                       'permissions__pid__url',
                                                                                       'permissions__menu_id',
                                                                                       'permissions__menu__title',
                                                                                       'permissions__menu__icon',
                                                                                       ).distinct()

    # 2、获取权限中的url放到列表中，因为session是无法处理queryset
    # permissions_list = [item['permissions__url'] for item in permissions_queryset]
    # 3、获取菜单信息+权限
    permissions_dict = {}
    menu_dict = {}
    for item in permissions_queryset:
        # 权限结构
        permissions_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid'],
            'p_title': item['permissions__pid__title'],
            'p_url': item['permissions__pid__url'],
        }

        # 菜单结构
        menu_id = item['permissions__menu_id']
        if not menu_id:
            continue
        # 每一个可做菜单的权限
        node = {'id': item['permissions__id'], 'title': item['permissions__title'], 'url': item['permissions__url']}
        if menu_id in menu_dict:
            menu_dict['permissions__menu_id']['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'url': item['permissions__menu__icon'],
                'children': [node, ]
            }

    # 3、放入session中
    request.session[settings.PERMISSIONS_SESSION_KEY] = permissions_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict

