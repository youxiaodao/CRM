#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/7 15:29
# @Author  : DollA
# @File    : study_record.py
# @Software: PyCharm
from crm import models
from stark.service.stark import site, StarkConfig, Option
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse, render,redirect
from django.urls import reverse
from django import forms
from django.db import transaction
from django.conf import settings
from django.forms import modelformset_factory


class StudyRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = ['student','record','score','homework_note']


class StudyRecordConfig(StarkConfig):

    def get_urls(self):
        urlpatterns = [
            url(r'^list/$', self.wrapper(self.changelist_view), name=self.get_url_name('changelist')),
        ]
        return urlpatterns

    def changelist_view(self, request):
        ccid = request.GET.get('ccid')
        model_formset_cls = modelformset_factory(models.StudyRecord, StudyRecordModelForm)
        queryset = models.StudyRecord.objects.filter(course_record_id=ccid)
        if request.method=='POST':
            formset=model_formset_cls(queryset=queryset,data=request.POST)
            if formset.is_valid():
                formset.save()
                return redirect('/stark/crm/studyrecord/list/?ccid=%s'%ccid)
            return render(request, 'study_record.html', {'formset': formset})
        # 实例化
        formset = model_formset_cls(queryset=queryset)
        return render(request, 'study_record.html', {'formset': formset})
