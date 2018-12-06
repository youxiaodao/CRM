from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from crm import models
from rbac.service.init_permission import init_permission


# 登陆
def login(request):
    # 1、用户登陆
    response = {}
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('pwd')

        current_user = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if not current_user:
            response['msg'] = '用户名或者密码错误'
            return render(request, 'login.html', locals())
        # 存入session
        request.session['user_info']={'id':current_user.id,'name':current_user.name}

        # 2、用户权限的初始化
        init_permission(request, current_user)

        return redirect('/stark/crm/course/list/')

    return render(request, 'login.html')
