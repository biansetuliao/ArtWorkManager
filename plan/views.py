from django.shortcuts import render
from django.views import generic
from login import views
from django.http import HttpResponse, HttpResponseRedirect


class IndexView(generic.View):
    templates_file = 'PlanIndex.html'

    def get(self, request):

        if request.user.is_authenticated():
            permission = views.user_permission(request, 'plan')
            if permission:
                return HttpResponseRedirect(permission)

        is_log_in = views.is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = {}

        return render(request,
                      self.templates_file,
                      context)