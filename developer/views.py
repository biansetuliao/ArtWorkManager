from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect


def is_sign_in(request):
    if not request.user.is_authenticated():
        return ('/?next=%s' % request.path)
    else:
        if request.user.has_perm('home.can_developer'):
            return
        else:
            return ('/login/menu')


class IndexView(generic.View):
    templates_file = 'DeveloperIndex.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = {}

        return render(request,
                      self.templates_file,
                      context)
