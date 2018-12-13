#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 16:45
# @Author  : DollA
# @Theme   : 权限校验中间件
import re
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限校验
    """

    def process_request(self, request):
        """
        当前用户请求刚进入时执行
        :param request:
        :return:
        """
        # 1、获取当前用户请求的URL - ------>request.path_info
        current_url = request.path_info

        # 在检验之前，先验证是不是在白名单中
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url,current_url):
                return None
            
        # 2、获取当前用户在session中保存的权限列表
        permission_dict = request.session.get(settings.PERMISSIONS_SESSION_KEY)
        if not permission_dict:
            return HttpResponse('未获取到用户权限信息，请登录！！')
        # 3、权限信息匹配,要用正则,还要加起始终止符
        flag = False
        
        url_record_list = [
            {'title': '首页', 'url': '#'}
        ]
        
        for item in permission_dict.values():
            reg = "^%s$" % item['url']
            if re.match(reg, current_url):
                flag = True

                # 在中间件，把数值传递到request中，用于inclusion_tag中选中菜单的判断和渲染
                request.current_selected_permission = item['pid'] or item['id']
                
                if not item['pid']:
                    url_record_list.extend([{'title': item['title'], 'url': item['url'], 'class':'active'}])
                else:
                    url_record_list.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class':'active'}
                    ])
                request.url_record_list = url_record_list
                break
        if not flag:
            return HttpResponse('无权访问！')



