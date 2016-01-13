# coding=utf-8

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from login import views


class LoginView(generic.View):
    templates_file = 'Login.html'

    def get(self, request):

        if request.user.is_authenticated():
            permission = views.user_permission(request, 'sign')
            if permission:
                return HttpResponseRedirect(permission)

        if 'error' in request.GET and request.GET['error']:
            error_code = request.GET['error']
            if error_code == '1':
                error_txt = "用户名不能为空"
            elif error_code == '2':
                error_txt = "密码不能为空"
            elif error_code == "3":
                error_txt = "很抱歉,该用户无访问权限!"
            elif error_code == "4":
                error_txt = "用户名与密码不匹配或该用户不存在!"
            else:
                error_txt = "未知错误,请与管理员联系!"
        else:
            error_txt = ""

        context = {
            "error_txt": error_txt
        }

        return render(request,
                      self.templates_file,
                      context)