#coding=utf8

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *


def is_sign_in(request):
    if not request.user.is_authenticated():
        return ('/?next=%s' % request.path)
    else:
        if request.user.has_perm('home.can_admin'):
            return
        else:
            return ('/login/menu')


class IndexView(generic.View):
    templates_file = 'Manager.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        groups = list(Group.objects.all())
        if groups:
            group_list = []
            for p in groups:
                a = {'id': p.id, 'code': p.code, 'name': p.name, 'format': p.format}
                group_list.append(a)
        else:
            group_list = []

        context = {
            'group_list': sorted(group_list, key=lambda x: x['code'])
        }

        return render(request,
                      self.templates_file,
                      context)


class TagView(generic.View):
    templates_file = 'ManagerTag.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        tags = list(Tag.objects.all().order_by("code"))
        if not tags:
            tags = []

        context = {
            'tags': tags
        }

        return render(request,
                      self.templates_file,
                      context)


# ADD


def create(request):

    if 'GInfo' in request.POST and request.POST['GInfo']:
        info_name = request.POST['GInfo']
    else:
        return HttpResponse("GInfo参数不存在!")

    # Code
    if 'code' in request.POST and request.POST['code']:
        code = request.POST['code']
    else:
        return HttpResponse("code参数不存在!")

    # Name
    if 'name' in request.POST and request.POST['name']:
        name = request.POST['name']
    else:
        return HttpResponse("name参数不存在!")

    # Group
    def group():

        if 'formate' in request.POST and request.POST['formate']:
            formate = request.POST['formate']
        else:
            return HttpResponse("formate参数不存在!")

        group_code = int(code)
        group_name = name

        add_group = Group(code=group_code,
                          name=group_name,
                          format=formate)
        add_group.save()

        return ('/manager/')

    # Tag
    def tag():

        tag_code = int(code)
        tag_name = name

        add_tag = Tag(code=tag_code,
                      name=tag_name)
        add_tag.save()

        return ('/manager/tag/')


    add = {
        "group": group,
        "tag": tag,
        # "ggt": ggt,
    }

    http = add[info_name]()
    return HttpResponseRedirect(http)
