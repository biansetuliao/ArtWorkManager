#coding=utf8

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *
from django.views.decorators.csrf import csrf_exempt

import simplejson


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

        group_list = list(Group.objects.all())

        context = {
            'group_list': group_list
        }

        return render(request,
                      self.templates_file,
                      context)


class GTTView(generic.View):
    templates_file = 'DeveloperGroup.html'

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


@csrf_exempt
def search_image(request):

    req = simplejson.loads(request.body)

    image_list = []
    for tag_name in req.keys():
        if tag_name == 'group':
            group_id = int(req[tag_name])
            id_by_group = []
            for p in list(Art.objects.filter(group=group_id, is_pass=1, is_audit=1)):
                id_by_group.append(p.id)
            image_list.append(id_by_group)
        else:
            tag_id = int(req[tag_name])
            tag_name = list(TagInfo.objects.filter(id=tag_id)).pop()
            id_by_tag = []
            for q in list(ArtInfo.objects.filter(tag=tag_id, value=tag_name.name)):
                id_by_tag.append(q.art.id)
            if id_by_tag:
                image_list.append(id_by_tag)

    x = image_list.pop()
    for art_id in image_list:
        if x != art_id:
            y = []
            for m in x:
                if m in art_id:
                    y.append(m)
            x = y

    art_list = []
    for p in x:
        for b in list(Art.objects.filter(id=p)):
            info_list = []
            for q in list(ArtInfo.objects.filter(pic_id=p)):
                import_info = {'name': q.tag.name, 'value': q.value}
                info_list.append(import_info)
                art_info = {'art_id': b.id, 'user': b.user, 'group': b.group, 'time': b.upload_time, 'version': b.version, 'preview': b.screen_shot, 'info_list': info_list}
            art_list.append(art_info)

    def artid(a):
        return a['art_id']

    artinfo_list = sorted(art_list, key=artid, reverse=True)

    context = {
        'artinfo_list': artinfo_list,
    }
    
    return render(request, 'DeveloperImage.html', context)