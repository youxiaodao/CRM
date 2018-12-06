#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/7 13:04
# @Author  : DollA
# @File    : student.py
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


class StudentConfig(StarkConfig):

    def display_class_list(self, row=None, isHeader=False):
        if isHeader:
            return "班级"
        class_list = row.class_list.all()
        class_name_list = ["%s%s期" % (row.course.name, row.semester) for row in class_list]
        return ','.join(class_name_list)

    list_display = ['username', 'customer', display_class_list]
