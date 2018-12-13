#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 23:32
# @Author  : DollA
# @Theme   : 静态菜单模板inclution_tag
import re
from collections import OrderedDict
from django.template import Library
from django.conf import settings

register = Library()


# @register.inclusion_tag('rbac/static_menu.html')
# def static_menu(request):
#     """
#     创建一级菜单
#     :return:
#     """
#     menu_list = request.session[settings.MENU_SESSION_KEY]
#     return {'menu_list': menu_list}


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    创建二级菜单
    :param request:
    :return:
    """
    menu_dict = request.session[settings.MENU_SESSION_KEY]

    # 对字典的额key进行排序
    key_list = sorted(menu_dict)

    # 创建空的有序字典
    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for per in val['children']:
            # regex = "^%s$" % per['url']
            # if re.match(regex, request.path_info):
            if per['id'] == request.current_selected_permission:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val

    return {'menu_dict': menu_dict}


@register.inclusion_tag('rbac/breadcumd.html')
def breadcumd(request):
    return {'url_record_list': request.url_record_list}


@register.filter
def has_permission(request, name):
    """
    判断是否有权限
    :param request: 请求参数相关
    :param name: 别名
    :return:
    """
    if name in request.session[settings.PERMISSIONS_SESSION_KEY]:
        return True
    return None
