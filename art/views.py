#coding=utf8

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *

import os
import re


def is_sign_in(request):
    if not request.user.is_authenticated():
        return ('/?next=%s' % request.path)
    else:
        if request.user.has_perm('home.can_art'):
            return
        else:
            return ('/login/menu/')


def art_count(request):

    user_id = request.user.id

    darts = list(Art.objects.filter(user=user_id, screen_shot="", resource_file=""))
    if darts:
        ddsc = len(darts)
    else:
        ddsc = 0
        darts = []

    sarts = list(Art.objects.filter(user=user_id, is_audit=0))
    if sarts:
        ddsh = int(len(sarts)) - int(ddsc)
    else:
        ddsh = 0
        sarts = []

    sart_list = []
    for p in sarts:
        if p not in darts:
            sart_list.append(p)

    parts = list(Art.objects.filter(user=user_id, is_audit=1, is_pass=1))
    if parts:
        psh = len(parts)
    else:
        psh = 0
        parts = []

    farts = list(Art.objects.filter(user=user_id, is_audit=1, is_pass=0))
    if farts:
        fsh = len(farts)
    else:
        fsh = 0
        farts = []

    context = {
        "darts": darts,
        "ddsc": ddsc,
        "sart_list": sart_list,
        "ddsh": ddsh,
        "parts": parts,
        "psh": psh,
        "farts": farts,
        "fsh": fsh,
    }

    return (context)


class IndexView(generic.View):
    templates_file = 'ArtIndex.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = art_count(request)

        return render(request,
                      self.templates_file,
                      context)


class ArtAuditView(generic.View):
    templates_file = 'ArtAudit.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = art_count(request)

        return render(request,
                      self.templates_file,
                      context)


class ArtPassView(generic.View):
    templates_file = 'ArtPass.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = art_count(request)

        return render(request,
                      self.templates_file,
                      context)


class ArtFaildView(generic.View):
    templates_file = 'ArtFaild.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = art_count(request)

        return render(request,
                      self.templates_file,
                      context)


class UploadTaskView(generic.View):
    templates_file = 'ArtUpload.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        if 'art_id' in request.GET and request.GET['art_id']:
            art_id = request.GET['art_id']
        else:
            return HttpResponse("Art ID错误!")

        arts = list(Art.objects.filter(id=int(art_id)))
        if arts:
            art_list = []
            for p in arts:
                artinfos = list(ArtInfo.objects.filter(art=p.id))
                if artinfos:
                    artinfo_list = []
                    for q in artinfos:
                        tag_name = list(GroupToTag.objects.filter(id=q.tag.id))
                        art_info = {"name": tag_name.pop().info, "value": q.value}
                        artinfo_list.append(art_info)
                else:
                    artinfo_list = []
                a = {"id": p.id, "group": p.group.name, "big_version": p.version, "description": p.description, 'art_info': artinfo_list}
                art_list.append(a)
        else:
            art_list = []

        context = {
            "art_list": art_list,
            "art_id": art_id,
        }

        return render(request,
                      self.templates_file,
                      context)


class UpdateUploadTaskView(generic.View):
    templates_file = 'ArtUpdateUpload.html'

    def get(self, request):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        context = {}

        return render(request,
                      self.templates_file,
                      context)


def upload(request):

    if "art_id" in request.POST and request.POST['art_id']:
        art_id = request.POST['art_id']
    else:
        return HttpResponse("Art ID不存在!")

    if "big_version" in request.POST and request.POST['big_version']:
        big_version = request.POST['big_version']
    else:
        return HttpResponse("Big_version 不存在!")

    if "preview" in request.FILES and request.FILES['preview']:
        screen_shot = request.FILES['preview']
    else:
        return HttpResponse("截图不存在!")

    if "resource" in request.FILES and request.FILES['resource']:
        resource = request.FILES['resource']
    else:
        return HttpResponse("资源不存在!")

    arts = list(Art.objects.filter(id=int(art_id)))
    if not arts:
        return HttpResponse("Art不存在!")

    # version

    art_list = []

    id_by_group = []
    for p in arts:
        groups = list(Art.objects.filter(group=p.group.id))
        for q in groups:
            id_by_group.append(q.id)
    art_list.append(id_by_group)

    artinfos = list(ArtInfo.objects.filter(art=int(art_id)))
    for p in artinfos:
        tags = list(ArtInfo.objects.filter(tag=p.tag.id, value=p.value))
        if tags:
            id_by_tag = []
            for q in tags:
                id_by_tag.append(q.art.id)
        else:
            id_by_tag = []
        art_list.append(id_by_tag)

    x = art_list.pop()
    for p in art_list:
        if x != p:
            y = []
            for q in x:
                if q in p:
                    y.append(q)
            x = y

    if not art_list:
        version = big_version + ".0"
    else:
        version_list = []
        for m in x:
            art_version = list(Art.objects.filter(id=m))
            versions = art_version.pop().version
            version_list.append(versions)

        version_info = []
        for p in version_list:
            it = re.finditer(r"\d+", p)
            num = []
            for match in it:
                b = match.group()
                num.append(b)
            if num[0] == big_version:
                version_info.append(p)

        if version_info:
            max_v = max(version_info)
            if max_v == big_version:
                version = str(num[0]) + "." + str(0)
            else:
                it = re.finditer(r"\d+", max_v)
                num = []
                for match in it:
                    a = match.group()
                    num.append(a)

                small_v = int(num[1]) + 1
                version = str(num[0]) + "." + str(small_v)
        else:
            version = big_version + ".0"

    for p in arts:

        # Determine upload file type
        format_type = p.group.format
        formal_type = os.path.splitext(resource.name)[1].lower()
        if not formal_type in (format_type):
            return HttpResponse('资源格式错误!')

        p.version = version
        p.screen_shot = screen_shot
        p.resource_file = resource
        p.save()

    return HttpResponseRedirect('/art/audit/')