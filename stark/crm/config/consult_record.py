#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/7 9:01
# @Author  : DollA
# @File    : consult_record.py
# @Software: PyCharm
from crm import models
from django.utils.safestring import mark_safe
# from django.urls import path
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django import forms
from django.db import transaction

from django.conf import settings
from stark.service.stark import StarkConfig, Option, get_chioce_text


class ConsultRecordConfig(StarkConfig):
    list_display = ['customer', 'note', 'consultant']

    def get_add_btn(self, display_type):
        return None

    def get_queryset(self):
        cid = self.request.GET.get('cid')
        if cid:
            return models.ConsultRecord.objects.filter(customer_id=cid)
        return models.ConsultRecord.objects


class PriModelForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        exclude = ['customer', 'consultant']


class PriConsultRecordConfig(StarkConfig):
    list_display = ['customer', 'note', 'consultant']

    model_form_class = PriModelForm

    def save(self, form, modify=False):
        if not modify:
            current_user_id = 1  # 当前客户
            prams = self.request.GET.get('_filter')
            cid, num = prams.split('=', maxsplit=1)

            form.instance.customer = models.Customer.objects.get(id=num)
            form.instance.consultant = models.UserInfo.objects.get(id=current_user_id)

        form.save()

    def get_queryset(self):
        cid = self.request.GET.get('cid')
        current_user_id = 1  # 当前客户
        if cid:
            return models.ConsultRecord.objects.filter(customer_id=cid, customer__consultant_id=current_user_id)
        return models.ConsultRecord.objects.filter(customer__consultant_id=current_user_id)

    # 获取定义表头的显示
    def get_list_display(self):
        val = []
        val.extend(self.list_display)
        val.append(StarkConfig.display_edit)  # 不能用self
        return val


class PubConsultRecordConfig(StarkConfig):
    list_display = ['customer', 'note', 'consultant']

    model_form_class = PriModelForm

    def get_add_btn(self, display_type):
        return None

    # 获取定义表头的显示
    def get_list_display(self):
        val = []
        val.extend(self.list_display)
        return val
