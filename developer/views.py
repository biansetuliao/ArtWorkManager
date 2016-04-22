#coding=utf8

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from home.models import *
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from wsgiref.util import FileWrapper

import simplejson
import mimetypes


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
            groups = list(Art.objects.filter(group=group_id, is_pass=1, is_audit=1))
            if groups:
                for p in groups:
                    id_by_group.append(p.id)
            else:
                id_by_group = []
            image_list.append(id_by_group)
        else:
            tag_id = int(req[tag_name])
            tag_name = list(TagInfo.objects.filter(id=tag_id))
            for p in tag_name:

                id_by_tag = []
                for q in list(ArtInfo.objects.filter(tag=p.tag.id, value=p.name)):
                    id_by_tag.append(q.art.id)

                if id_by_tag:
                    image_list.append(id_by_tag)
                else:
                    id_by_tag = []
                    image_list.append(id_by_tag)

    x = image_list.pop()
    for art_id in image_list:
        if x != art_id:
            y = []
            for m in x:
                if m in art_id:
                    y.append(m)
            x = y

    if x:

        art_list = []
        for p in x:
            for b in list(Art.objects.filter(id=p)):
                info_list = []
                for q in list(ArtInfo.objects.filter(art=int(p))):
                    import_info = {'name': q.tag.name, 'value': q.value}
                    info_list.append(import_info)

                # 计算图片显示比例
                img = Image.open(b.screen_shot)
                with img as im:
                    width, height = im.size
                if width > height:
                    scale = "100%"
                    if height > 300:
                        scale = "50%"
                else:
                    scale = "50%"

                art_info = {'art_id': b.id, 'user': b.user, 'group': b.group, 'time': b.upload_time, 'version': b.version, 'preview': b.screen_shot, 'scale': scale, 'info_list': info_list}
                art_list.append(art_info)

        def artid(a):
            return a['art_id']

        artinfo_list = sorted(art_list, key=artid, reverse=True)

    else:

        artinfo_list = []

    context = {
        'artinfo_list': artinfo_list,
    }
    
    return render(request, 'DeveloperImage.html', context)


def download(request):

    if 'group_id' in request.GET and request.GET['group_id']:
        group_id = request.GET['group_id']
    else:
        return HttpResponse("Group ID 错误或不存在!")

    if 'art_id' in request.GET and request.GET['art_id']:
        art_id = request.GET['art_id']
    else:
        return HttpResponse("Art ID 错误或不存在!")

    arts = list(Art.objects.filter(id=int(art_id)))
    if not arts:
        return HttpResponse("ArtID错误或不存在!")

    groups = list(Group.objects.filter(id=int(group_id)))
    if not groups:
        return HttpResponse("Group ID 错误或不存在!")

    orders = list(TagOrder.objects.filter(group=int(group_id)).order_by('sort'))

    # Data conversion
    def conversion(x):
        a = hex(int(x))
        b = a[2:]
        c = b.zfill(3)
        return c

    # Filename
    if orders:
        filename_list = []
        for p in orders:
            if p.code == 'group':
                f = conversion(groups.pop().code)
                filename_list.append(f)
            else:
                tags = list(Tag.objects.filter(name=p.code))
                if not tags:
                    return HttpResponse("Tag不存在!")

                art_info = list(ArtInfo.objects.filter(art=int(art_id), tag=int(tags.pop().id)))
                if art_info:
                    for p in art_info:
                        tag_code = list(TagInfo.objects.filter(tag=int(p.tag.id), name=p.value))
                        f = conversion(tag_code.pop().code)
                        filename_list.append(f)
                else:
                    f = conversion(0)
                    filename_list.append(f)
    else:
        filename_list = []
        f = conversion(groups.pop().code)
        filename_list.append(f)

        art_info = list(ArtInfo.objects.filter(art=int(art_id)))
        if not art_info:
            return HttpResponse("Art ID 错误或不存在!")

        for p in art_info:
            tag_code = list(TagInfo.objects.filter(tag=int(p.tag.id), name=p.value))
            f = conversion(tag_code.pop().code)
            filename_list.append(f)

    file_name = ""
    for q in filename_list:
        file_name += str(q)

    formats = list(Group.objects.filter(id=int(group_id)))
    if not formats:
        return HttpResponse("Group ID 错误或不存在!")

    filename = file_name + formats.pop().format

    # Download
    arts = list(Art.objects.filter(id=int(art_id)))
    if not arts:
        return HttpResponse("Art ID 错误或不存在!")

    for p in arts:

        url = p.resource_file.path
        wrapper = FileWrapper(open(url, 'rb'))
        content_type = mimetypes.guess_type(url)
        response = HttpResponse(wrapper, content_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        return response