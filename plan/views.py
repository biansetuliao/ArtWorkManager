from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *


def is_sign_in(request):
    if not request.user.is_authenticated():
        return ('/?next=%s' % request.path)
    else:
        if request.user.has_perm('home.can_plan'):
            return
        else:
            return ('/login/menu')


class IndexView(generic.View):
    templates_file = 'PlanIndex.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        group_list = list(Group.objects.all())

        context = {
            'group_list': group_list
        }

        return render(request,
                      self.templates_file,
                      context)