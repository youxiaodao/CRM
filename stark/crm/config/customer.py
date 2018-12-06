#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/6 17:30
# @Author  : DollA
# @File    : customer.py
# @Software: PyCharm
from crm import models
from django.utils.safestring import mark_safe
# from django.urls import path
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django import forms
from django.db import transaction
from django.db.models.fields.related import ForeignKey, ManyToManyField

from django.conf import settings
from stark.service.stark import StarkConfig, Option, get_chioce_text,Row


# 组合搜索的时候，自定制显示的条件的去重，有一样的，只显示一个
class DistinctNameOption(Option):

    def get_queryset(self, _field, model_class, query_dict):
        row = Row(model_class.objects.filter(**self.condition).values_list('name').distinct(), self, query_dict)
        return row


class CustomerConfig(StarkConfig):

    # 跟进记录
    def display_follow(self, row=None, isHeader=False):
        """
        跟进记录
        :param row:
        :param isHeader:
        :return:
        """
        if isHeader:
            return '跟进记录'
        url = reverse('stark:crm_consultrecord_changelist')
        return mark_safe('<a href="%s?cid=%s">跟进记录</a>' % (url, row.pk))

    list_display = ['name', 'qq',
                    get_chioce_text('状态', 'status'),
                    get_chioce_text('性别', 'gender'),
                    get_chioce_text('客户来源', 'source'),
                    display_follow,
                    ]

    order_by = ['-id']  # -id 是时间的倒叙

    search_list = ['name']

    filter_list = [
        DistinctNameOption('name',condition={'id__gt':9},value_func=lambda x:x[0],text_func=lambda x:x[0]),
        Option('status', isChoice=True, text_func=lambda x: x[1]),
        Option('source', isChoice=True, text_func=lambda x: x[1]),
        Option('gender', isChoice=True, text_func=lambda x: x[1])
    ]


class PubModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        # fields=[]
        # fields='__all__'
        exclude = ['consultant', 'status']


class PubliscCustomerConfig(StarkConfig):
    # 跟进记录
    def display_follow(self, row=None, isHeader=False):
        """
        跟进记录
        :param row:
        :param isHeader:
        :return:
        """
        if isHeader:
            return '跟进记录'
        url = reverse('stark:crm_consultrecord_pub_changelist')
        return mark_safe('<a href="%s?cid=%s">跟进记录</a>' % (url, row.pk))

    list_display = ['name', 'qq',
                    get_chioce_text('状态', 'status'),
                    get_chioce_text('性别', 'gender'),
                    get_chioce_text('客户来源', 'source'),
                    display_follow,
                    ]

    order_by = ['-id']  # -id 是时间的倒叙

    search_list = ['name']

    filter_list = [
        Option('status', isChoice=True, text_func=lambda x: x[1]),
        Option('source', isChoice=True, text_func=lambda x: x[1]),
        Option('gender', isChoice=True, text_func=lambda x: x[1])
    ]

    model_form_class = PubModelForm

    def get_queryset(self):
        return self.model_class.objects.filter(consultant__isnull=True)

    # 获取定义表头的显示
    def get_list_display(self):
        val = []
        val.extend(self.list_display)
        val.append(StarkConfig.display_edit)  # 不能用self
        val.insert(0, StarkConfig.display_checkbox)
        # val=super().get_list_display()
        # val.remove(StarkConfig.display_del)
        return val

    # 申请客户
    def multi_apply(self, request):
        """
        申请客户
        :param request:
        :return:
        """

        current_user_id = 1
        id_list = request.POST.getlist('pk')

        my_customer_count = models.Customer.objects.filter(consultant_id=current_user_id, status=2).count()
        if my_customer_count + len(id_list) > settings.MAX_PRIVATE_CUSTOMER:
            return HttpResponse('超过最大客户数量，添加失败')

        # 事务
        flag = False
        with transaction.atomic():
            # select_for_update上锁
            origin = models.Customer.objects.filter(id__in=id_list, consultant__isnull=True).select_for_update()
            if origin.count() == len(id_list):
                models.Customer.objects.filter(id__in=id_list).update(consultant=current_user_id)
                flag = True
        if not flag:
            return HttpResponse('已被申请')

    multi_apply.text = '申请客户'
    action_list = [multi_apply]


class PriModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        # fields=[]
        # fields='__all__'
        exclude = ['consultant', 'status']


class PrivateCustomerConfig(StarkConfig):

    # 跟进记录
    def display_follow(self, row=None, isHeader=False):
        """
        跟进记录
        :param row:
        :param isHeader:
        :return:
        """
        if isHeader:
            return '跟进记录'
        url = reverse('stark:crm_consultrecord_pri_changelist')
        return mark_safe('<a href="%s?cid=%s">跟进记录</a>' % (url, row.pk))

    list_display = ['name', 'qq',
                    get_chioce_text('状态', 'status'),
                    get_chioce_text('性别', 'gender'),
                    get_chioce_text('客户来源', 'source'),
                    display_follow,
                    ]

    order_by = ['-id']  # -id 是时间的倒叙

    search_list = ['name']

    filter_list = [
        Option('status', isChoice=True, text_func=lambda x: x[1]),
        Option('source', isChoice=True, text_func=lambda x: x[1]),
        Option('gender', isChoice=True, text_func=lambda x: x[1])
    ]

    model_form_class = PriModelForm

    def get_queryset(self):
        current_user_id = 1
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self, form, modify=False):
        current_user_id = 1
        # instance表示自己当前的对象
        form.instance.consultant = models.UserInfo.objects.get(id=current_user_id)

        return form.save()

    # 获取定义表头的显示
    def get_list_display(self):
        val = []
        val.extend(self.list_display)
        val.append(StarkConfig.display_edit)  # 不能用self
        val.insert(0, StarkConfig.display_checkbox)
        # val=super().get_list_display()
        # val.remove(StarkConfig.display_del)
        return val

    # 移除客户
    def multi_remove(self, request):
        id_list = request.POST.getlist('pk')
        current_user_id = 1
        models.Customer.objects.filter(id__in=id_list, consultant_id=current_user_id, status=2).update(consultant=None)

    multi_remove.text = '移除客户'
    action_list = [multi_remove]
