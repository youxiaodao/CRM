from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from stark.service.stark import StarkConfig, get_chioce_text,Option



class UserInfoConfig(StarkConfig):

    # 查看详细
    def display_detail(self, row=None, isHeader=False):
        if isHeader:
            return '查看详情'
        reverse_url = reverse('stark:crm_userinfo_detail', kwargs={'pk': row.id})
        return mark_safe('<a href="%s">%s</a>' % (reverse_url, row.name))

    # 扩展查看详情的URL
    def extra_url(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        urlpatterns = [
            url(r'^(?P<pk>\d+)/detail/$', self.wrapper(self.detail_view), name='%s_%s_detail' % info),
        ]
        return urlpatterns

    # 查看详情的视图
    def detail_view(self, request, pk):

        return HttpResponse('查看详情')

    list_display = [display_detail,get_chioce_text('性别','gender'), 'phone', 'email', 'depart', StarkConfig.display_del_edit]
    search_list = ['name', 'depart__title']
