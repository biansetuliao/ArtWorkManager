from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


def user_permission(request, rank):

    if request.user.has_perm('home.can_admin'):
        if rank in ['art', 'plan', 'developer', 'admin']:
            return
        else:
            return ('/manager')
    else:
        if request.user.has_perm('home.can_art'):
            if rank == "art":
                return
            else:
                return ('/art')
        elif request.user.has_perm('home.can_plan'):
            if rank == "plan":
                return
            else:
                return ('/plan')
        elif request.user.has_perm('home.can_developer'):
            if rank == "developer":
                return
            else:
                return ('/developer')
        else:
            if rank == "sign":
                return
            else:
                return ('/?error=3')


def is_sign_in(request):
    if not request.user.is_authenticated():
        return ('/?next=%s' % request.path)
    else:
        return


def sign_in(request):

    if 'username' in request.POST and request.POST['username']:
        username = request.POST['username']
    else:
        return HttpResponseRedirect('/?error=1')

    if 'password' in request.POST and request.POST['password']:
        password = request.POST['password']
    else:
        return HttpResponseRedirect('/?error=2')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        permission = user_permission(request, 'sign')
        if permission:
            return HttpResponseRedirect(permission)
        else:
            return HttpResponseRedirect('/?error=3')
    else:
        return HttpResponseRedirect('/?error=4')


def sign_out(request):

    logout(request)

    return HttpResponseRedirect('/')