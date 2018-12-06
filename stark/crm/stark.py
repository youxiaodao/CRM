#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/5 14:23
# @Author  : DollA
# @File    : stark.py
# @Software: PyCharm
from crm import models
from django.utils.safestring import mark_safe
# from django.urls import path
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse

from stark.service.stark import site, StarkConfig
from crm.config import class_list
from crm.config import userinfo
from crm.config import customer
from crm.config import consult_record, student, course_record, study_record


class DepartMentConfig(StarkConfig):
    list_display = ['id', 'title', StarkConfig.display_del_edit]


class CourseConfig(StarkConfig):
    list_display = ['id', 'name', StarkConfig.display_del_edit]


class SchoolConfig(StarkConfig):
    list_display = ['id', 'title', StarkConfig.display_del_edit]


site.registry(models.Department, DepartMentConfig)
site.registry(models.UserInfo, userinfo.UserInfoConfig)
site.registry(models.Course, CourseConfig)
site.registry(models.School, SchoolConfig)
site.registry(models.ClassList, class_list.ClasslistConfig)

site.registry(models.Customer, customer.CustomerConfig)
site.registry(models.Customer, customer.PubliscCustomerConfig, 'pub')
site.registry(models.Customer, customer.PrivateCustomerConfig, 'pri')

site.registry(models.ConsultRecord, consult_record.ConsultRecordConfig)
site.registry(models.ConsultRecord, consult_record.PriConsultRecordConfig, 'pri')
site.registry(models.ConsultRecord, consult_record.PubConsultRecordConfig, 'pub')

site.registry(models.Student, student.StudentConfig)

site.registry(models.CourseRecord, course_record.CourseRecordConfig)

site.registry(models.StudyRecord, study_record.StudyRecordConfig)
