#coding=utf8

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *
from django.views.decorators.csrf import csrf_exempt

import simplejson
import re


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


class GTTView(generic.View):
    templates_file = 'ajax/PlanGroup.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        if 'group_id' in request.GET and request.GET['group_id']:
            group_id = request.GET['group_id']
        else:
            return HttpResponse('Group ID 错误或不存在!')

        groups = list(Group.objects.filter(id=int(group_id)))
        if not groups:
            return HttpResponse('Group 不存在 或 Group ID 错误!')

        gtts = list(GroupToTag.objects.filter(group=int(group_id)))
        if not gtts:
            gtts = []
            gtt_list = []
        else:
            gtt_list = []
            for p in gtts:
                tag_id = int(p.tag.id)
                taginfos = list(TagInfo.objects.filter(group=int(group_id), tag=tag_id))
                if taginfos:
                    tag_info = {'name': p.tag.name, 'info': p.info, 'info_list': taginfos}
                else:
                    tag_info = {}
                gtt_list.append(tag_info)


        context = {
            'group_id': group_id,
            'group_name': groups.pop().name,
            'gtts': gtts,
            'gtt_list': gtt_list,
        }

        return render(request,
                      self.templates_file,
                      context)


class PlanAdminView(generic.View):
    templates_file = 'PlanAdmin.html'

    def get(self, request):

        context = {}

        return render(request,
                      self.templates_file,
                      context)


class PlanAuditView(generic.View):
    templates_file = 'PlanAudit.html'

    def get(self, request):

        context = {}

        return render(request,
                      self.templates_file,
                      context)


class YAuditTaskView(generic.View):
    templates_file = 'YAuditTask.html'

    def get(self, request):

        context = {}

        return render(request,
                      self.templates_file,
                      context)


class AuditTaskView(generic.View):
    templates_file = 'AuditTask.html'

    def get(self, request):

        context = {}

        return render(request,
                      self.templates_file,
                      context)


@csrf_exempt
def search_bv(request):

    req = simplejson.loads(request.body)

    version_list = []
    for tag_name in req.keys():
        if tag_name == 'group':
            group_id = int(req[tag_name])
            version_by_group = []
            for p in list(Art.objects.filter(group=group_id)):
                version_by_group.append(p.version)
            version_list.append(version_by_group)
        else:
            tag_id = int(req[tag_name])
            tag_name = list(TagInfo.objects.filter(id=tag_id)).pop()
            version_by_tag = []
            for q in list(ArtInfo.objects.filter(tag=tag_id, value=tag_name.name)):
                version_by_tag.append(q.art.version)
            if version_by_tag:
                version_list.append(version_by_tag)

    x = version_list.pop()
    for version_num in version_list:
        if x != version_num:
            y = []
            for m in x:
                if m in version_num:
                    y.append(m)
            x = y

    bv_info = []
    for p in x:
        it = re.finditer(r"\d+", p)
        num = []
        for match in it:
            b = match.group()
            num.append(b)
        bv_info.append(num[0])

    if bv_info:
        max_bv = max(bv_info) + 1
        n = 1
        bv_list = []
        while n <= max_bv:
            bv_list.append(n)
            n = n + 1
    else:
        bv_list = [1]

    context = {
        'bv_list': bv_list,
    }

    return render(request, 'ajax/PlanVersion.html', context)
