#coding=utf8

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

import simplejson
import re
import time


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

        users = list(User.objects.all())
        user_list = []
        for p in users:
            if p.has_perm('home.can_art'):
                a = {'id': p.id, 'username': p.username}
                user_list.append(a)

        context = {
            'group_list': group_list,
            'user_list': user_list,
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

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        # img null
        narts = list(Art.objects.filter(screen_shot="", resource_file=""))
        if narts:
            nimg = len(narts)
        else:
            narts = []
            nimg = 0

        # img not null
        yarts = list(Art.objects.all())
        if yarts:
            yimg = len(yarts) - nimg
        else:
            yimg = 0

        context = {
            'narts': narts,
            'nimg': nimg,
            'yimg': yimg,
        }

        return render(request,
                      self.templates_file,
                      context)


class PlanAuditView(generic.View):
    templates_file = 'PlanAudit.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        yarts = list(Art.objects.filter(screen_shot="", resource_file=""))
        if not yarts:
            yarts = []
        warts = list(Art.objects.filter(is_audit=0))
        if not warts:
            warts = []

        wsh_list = []
        for p in warts:
            if p not in yarts:
                wsh_list.append(p)

        wsh = len(wsh_list)

        parts = list(Art.objects.filter(is_audit=1, is_pass=1))
        if parts:
            psh = len(parts)
        else:
            psh = 0

        farts = list(Art.objects.filter(is_audit=1, is_pass=0))
        if farts:
            fsh = len(farts)
        else:
            fsh = 0

        context = {
            'warts': wsh_list,
            'wsh': wsh,
            'psh': psh,
            'fsh': fsh,
        }

        return render(request,
                      self.templates_file,
                      context)


class AuditTaskView(generic.View):
    templates_file = 'AuditTask.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = {}

        return render(request,
                      self.templates_file,
                      context)


class PassTaskView(generic.View):
    templates_file = 'PassTask.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        parts = list(Art.objects.filter(is_audit=1, is_pass=1))
        if not parts:
            parts = []

        context = {
            'parts': parts,
        }

        return render(request,
                      self.templates_file,
                      context)


class FaildTaskView(generic.View):
    templates_file = 'FaildTask.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        farts = list(Art.objects.filter(is_audit=1, is_pass=0))
        if not farts:
            farts = []

        context = {
            'farts': farts,
        }

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
        max_bv = int(max(bv_info)) + 1
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


def create_task(request):

    if request.method == 'GET':
        return HttpResponse("request method error")

    if 'group' in request.POST and request.POST['group']:
        group_id = request.POST['group']
        groups = list(Group.objects.filter(id=int(group_id))).pop()
    else:
        return HttpResponse("error in group")

    if 'username' in request.POST and request.POST['username']:
        user_id = request.POST['username']
        users = list(User.objects.filter(id=int(user_id))).pop()
    else:
        return HttpResponse("error in username")

    if 'big_version' in request.POST and request.POST['big_version']:
        big_version = request.POST['big_version']
    else:
        return HttpResponse("error in big_version")

    if 'priority' in request.POST and request.POST['priority']:
        priority = request.POST['priority']
    else:
        return HttpResponse("error in priority")

    if 'description' in request.POST and request.POST['description']:
        description = request.POST['description']
    else:
        return HttpResponse("error in description")

    pub_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    tags = GroupToTag.objects.filter(group=group_id)
    if not tags:
        return HttpResponse("error in tags")

    #upload
    up_art = Art(user=users,
                 group=groups,
                 upload_time=pub_date,
                 version=int(big_version),
                 description=description,
                 priority=priority)
    up_art.save()

    #upload info
    art_id = up_art.id
    art = list(Art.objects.filter(id=art_id)).pop()
    for p in tags:
        tag_values = request.POST[p.group.name + '_' + p.tag.name]
        tag_object = list(Tag.objects.filter(id=p.tag.id)).pop()
        up_info = ArtInfo(art=art,
                          tag=tag_object,
                          value=tag_values)
        up_info.save()

    return HttpResponseRedirect("/plan/")


def del_task(request):

    if 'art_id' in request.GET and request.GET['art_id']:
        art_id = request.GET['art_id']
    else:
        return HttpResponse("Art ID 不存在或错误!")

    arts = Art.objects.filter(id=int(art_id))
    if arts:
        arts.delete()
    else:
        return HttpResponse("任务不存在或Art ID 错误!")

    return HttpResponseRedirect('/plan/admin_plan/')