from crm import models
from django.utils.safestring import mark_safe
# from django.urls import path
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse

from stark.service.stark import StarkConfig, Option


class ClasslistConfig(StarkConfig):

    def display_semester_title(self, row=None, isHeader=False):
        """

        :param row:
        :param isHeader:
        :return:
        """
        if isHeader:
            return '班级'
        return '%s-%s期' % (row.course.name, row.semester)

    def display_start_date(self, row=None, isHeader=False):
        if isHeader:
            return '开班日期'
        return row.start_date.strftime('%Y-%m-%d')

    list_display = ['id', display_semester_title, 'school', display_start_date, StarkConfig.display_del_edit]
    filter_list = [
        Option(field='school'),
        Option(field='course'),

    ]
