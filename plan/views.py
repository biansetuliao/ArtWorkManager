#coding=utf8

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from wsgiref.util import FileWrapper
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import simplejson
import re
import time
import mimetypes


def is_sign_in(request):
    if not request.user.is_authenticated():
        return ('/?next=%s' % request.path)
    else:
        if request.user.has_perm('home.can_plan'):
            return
        else:
            return ('/login/menu')


def pagination(request, number, target):

    paginator = Paginator(target, number)
    page = request.GET.get('page')
    try:
        target = paginator.page(page)
    except PageNotAnInteger:
        target = paginator.page(1)
    except EmptyPage:
        target = paginator.page(paginator.num_pages)

    return (target)


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
        nart_list = list(Art.objects.filter(screen_shot="", resource_file=""))
        if nart_list:
            narts = pagination(request, 10, nart_list)
            nimg = len(nart_list)
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


def count(request):

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

    if wsh_list:
        wsh = len(wsh_list)
        wshs = pagination(request, 10, wsh_list)
    else:
        wsh = 0
        wshs = []

    part_list = list(Art.objects.filter(is_audit=1, is_pass=1))
    if part_list:
        psh = len(part_list)
        parts = pagination(request, 10, part_list)
    else:
        psh = 0
        parts = []

    fart_list = list(Art.objects.filter(is_audit=1, is_pass=0))
    if fart_list:
        fsh = len(fart_list)
        farts = pagination(request, 10, fart_list)
    else:
        fsh = 0
        farts = []

    context = {
        'wsh': wsh,
        'psh': psh,
        'fsh': fsh,
        'wshs': wshs,
        'parts': parts,
        'farts': farts,
    }

    return context


class PlanAuditView(generic.View):
    templates_file = 'PlanAudit.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = count(request)

        return render(request,
                      self.templates_file,
                      context)


class AuditTaskView(generic.View):
    templates_file = 'AuditTask.html'

    def get(self, request, art_id):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        arts = list(Art.objects.filter(id=int(art_id)))
        if not arts:
            return HttpResponse("Art ID错误或不存在!")

        art_list = []
        for p in arts:
            artinfos = list(ArtInfo.objects.filter(id=p.id))
            if not artinfos:
                return HttpResponse("ArtInfo不存在!")
            a = {"id": p.id,
                 "group": p.group,
                 "version": p.version,
                 "preview": p.screen_shot,
                 "resource": p.resource_file,
                 "decription": p.description,
                 "artinfo": artinfos,
                 "user": p.user.username,}
            art_list.append(a)

        context = {
            "art_id": art_id,
            "art_list": art_list,
        }

        return render(request,
                      self.templates_file,
                      context)


class PassTaskView(generic.View):
    templates_file = 'PassTask.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = count(request)

        return render(request,
                      self.templates_file,
                      context)


class FaildTaskView(generic.View):
    templates_file = 'FaildTask.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = count(request)

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
        tag_id = request.POST[p.group.name + '_' + p.tag.name]
        tag_object = list(Tag.objects.filter(id=p.tag.id)).pop()
        tag_values = list(TagInfo.objects.filter(id=int(tag_id)))
        for p in tag_values:
            up_info = ArtInfo(art=art,
                              tag=tag_object,
                              value=p.name)
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


def download(request):

    if "art_id" in request.POST and request.POST['art_id']:
        art_id = request.POST['art_id']
    else:
        return HttpResponse("ArtID1错误或不存在!")

    #download
    arts = list(Art.objects.filter(id=int(art_id)))
    if not arts:
        return HttpResponse("ArtID错误或不存在!")

    for p in arts:

        url = p.resource_file.path
        f = re.compile(r'[^/]+$')
        match = f.search(url)
        if match:
            filename = match.group()
        else:
            return HttpResponse("文件名错误!")
        wrapper = FileWrapper(open(url, 'rb'))
        content_type = mimetypes.guess_type(url)
        response = HttpResponse(wrapper, content_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        return response


def audit(request):

    if "art_id" in request.POST and request.POST['art_id']:
        art_id = request.POST['art_id']
    else:
        return HttpResponse("ArtID不存在!")

    if "is_pass" in request.POST and request.POST['is_pass']:
        is_pass = request.POST['is_pass']
    else:
        return HttpResponse("请选择该资源是否通过审核!")

    arts = list(Art.objects.filter(id=int(art_id)))
    if not arts:
        return HttpResponse("ArtID错误!")

    if "0" == is_pass:

        if "reason" in request.POST and request.POST['reason']:
            reason = request.POST['reason']
        else:
            return HttpResponse('未通过审核原因不能为空!')

        for p in arts:
            p.is_audit = 1
            p.is_pass = 0
            p.reason = reason
            p.save()

        return HttpResponseRedirect("/plan/faild_task/")

    elif "1" == is_pass:

        for p in arts:
            p.is_audit = 1
            p.is_pass = 1
            p.save()

        return HttpResponseRedirect("/plan/pass_task/")

    else:
        return HttpResponse("审核失败!")