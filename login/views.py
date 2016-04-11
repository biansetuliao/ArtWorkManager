from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


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
        if request.user.has_perms(['home.can_admin', 'home.can_developer', 'home.can_art', 'home.can_plan']):
            return HttpResponseRedirect('/login/menu')
        else:
            return HttpResponseRedirect('/?error=3')
    else:
        return HttpResponseRedirect('/?error=4')


def sign_out(request):

    logout(request)

    return HttpResponseRedirect('/')


class MenuViews(generic.View):
    templates_file = 'Menu.html'

    def get(self, request):

        if not request.user.is_authenticated():
            return HttpResponseRedirect('/?next=%s' % request.path)

        context = {}

        return render(request,
                      self.templates_file,
                      context)