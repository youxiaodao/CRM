#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/1 11:03
# @Author  : DollA
# @File    : stark.py
# @Software: PyCharm
from django.template import Library
from types import FunctionType
register=Library()


def header_list(cl):
    """
    数据列表页面，显示表头
    :param cl: 封装了要显示的数据列表的属性，stark中的类名为ChangeListParameters
    :return:
    """
    # 表头
    if cl.list_display:
        for name_or_func in cl.list_display:
            if isinstance(name_or_func, FunctionType):
                verbase_name = name_or_func(cl.config, isHeader=True)
            else:
                # 显示表模型field字段的verbose_name
                verbase_name = cl.config.model_class._meta.get_field(name_or_func).verbose_name
            yield verbase_name
    # 没有定制展示display_list，就直接显示表名
    else:
        yield cl.config.model_class._meta.model_name

def body_list(cl):
    # 表数据
    for row in cl.queryset:
        row_list = []
        # 如果没有定制展示display_list，数据直接放入对象，然后打印
        if not cl.list_display:
            row_list.append(row)
            yield row_list
            continue
        for name_or_func in cl.list_display:
            if isinstance(name_or_func, FunctionType):
                val = name_or_func(cl.config, row=row)
                print(val)
            else:
                val = getattr(row, name_or_func)

            row_list.append(val)
        yield row_list


@register.inclusion_tag('stark/table.html')
def table(cl):
    """
    显示数据列表
    :param cl: 传参数的类
    :return:
    """

    return {'header_list':header_list(cl),'body_list':body_list(cl)}