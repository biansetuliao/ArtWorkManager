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

        groups = list(Group.objects.all().order_by('code'))
        if groups:
            group_list = []
            for p in groups:
                a = {'id': p.id, 'code': p.code, 'name': p.name, 'format': p.format}
                group_list.append(a)
        else:
            group_list = []

        if 'error' in request.GET and request.GET['error']:
            error_code = request.GET['error']
        else:
            error_code = '0'

        if error_code == '1':
            error_txt = '添加失败!编号不能为空,不能重复,只能是数字!'
        elif error_code == '2':
            error_txt = '添加失败!名称不能为空!'
        elif error_code == '3':
            error_txt = '添加失败!文件类型不能为空或该类型不存在!'
        else:
            error_txt = ''

        context = {
            'group_list': sorted(group_list, key=lambda x: x['code']),
            'error_txt': error_txt,
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

        tag_list = list(Tag.objects.all().order_by("code"))
        if not tag_list:
            tag_list = []

        if 'error' in request.GET and request.GET['error']:
            error_code = request.GET['error']
        else:
            error_code = '0'

        if error_code == '1':
            error_txt = '添加失败!编号不能为空,不能重复,只能是数字!'
        elif error_code == '2':
            error_txt = '添加失败!名称不能为空!'
        else:
            error_txt = ''

        context = {
            'tag_list': tag_list,
            'error_txt': error_txt
        }

        return render(request,
                      self.templates_file,
                      context)


class TagUpdateView(generic.View):
    templates_file = 'TagUpdate.html'

    def get(self, request, tag_id):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        tags = list(Tag.objects.filter(id=int(tag_id)))
        if not tags:
            return HttpResponseRedirect('/manager/tag')

        if 'error' in request.GET and request.GET['error']:
            error_code = request.GET['error']
        else:
            error_code = '0'

        if error_code == '1':
            error_txt = '更新失败!编号不能为空,不能重复,只能是数字!'
        elif error_code == '2':
            error_txt = '更新失败!名称不能为空!'
        elif error_code == '3':
            error_txt = '更新失败!Tag ID错误或不存在!'
        else:
            error_txt = ''

        context = {
            'tags': tags,
            'error_txt': error_txt
        }

        return render(request,
                      self.templates_file,
                      context)


class GroupUpdateView(generic.View):
    templates_file = 'GroupUpdate.html'

    def get(self, request, group_id):

        is_log_in = is_sign_in(request)
        if is_log_in:
            return HttpResponseRedirect(is_log_in)

        groups = list(Group.objects.filter(id=int(group_id)))
        if not groups:
            return HttpResponseRedirect('/manager')

        tags = list(Tag.objects.all())

        gtt_list = list(GroupToTag.objects.filter(group=int(group_id)))
        if not gtt_list:
            gtt_list = []

        if 'error' in request.GET and request.GET['error']:
            error_code = request.GET['error']
        else:
            error_code = '0'

        if error_code == '1':
            error_txt = '更新失败!编号不能为空,不能重复,只能是数字!'
        elif error_code == '2':
            error_txt = '更新失败!名称不能为空!'
        elif error_code == '3':
            error_txt = '更新失败!文件类型不能为空或该类型不存在!'
        elif error_code == '4':
            error_txt = '更新失败!Group ID错误或不存在!'
        else:
            error_txt = ''

        context = {
            'groups': groups,
            'tags': tags,
            'gtt_list': gtt_list,
            'group_id': group_id,
            'error_txt': error_txt
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

    # Group
    def group():

        # Code
        if 'code' in request.POST and request.POST['code']:
            code = request.POST['code']
        else:
            return ('/manager/?error=1')

        # Name
        if 'name' in request.POST and request.POST['name']:
            name = request.POST['name']
        else:
            return ('/manager/?error=2')

        # Format
        if 'format' in request.POST and request.POST['format']:
            format = request.POST['format']
        else:
            return ("/manager/?error=3")

        group_code = int(code)
        group_name = name

        add_group = Group(code=group_code,
                          name=group_name,
                          format=format)
        add_group.save()

        return ('/manager/')

    # Tag
    def tag():

        # Code
        if 'code' in request.POST and request.POST['code']:
            code = request.POST['code']
        else:
            return ('/manager/tag/?error=1')

        # Name
        if 'name' in request.POST and request.POST['name']:
            name = request.POST['name']
        else:
            return ('/manager/tag/?error=2')

        tag_code = int(code)
        tag_name = name

        add_tag = Tag(code=tag_code,
                      name=tag_name)
        add_tag.save()

        return ('/manager/tag/')


    add = {
        "group": group,
        "tag": tag,
    }

    http = add[info_name]()
    return HttpResponseRedirect(http)


# Update


def update(request):

    if 'GInfo' in request.POST and request.POST['GInfo']:
        info_name = request.POST['GInfo']
    else:
        return HttpResponse("GInfo参数不存在!")

    # id
    if 'GID' in request.POST and request.POST['GID']:
        info_id = request.POST['GID']
    else:
        return HttpResponse("GID参数不存在!")

    #Group
    def group():

        # Code
        if 'code' in request.POST and request.POST['code']:
            code = request.POST['code']
        else:
            return ('/manager/updategroup/%d/?error=1' % int(info_id))

        # Name
        if 'name' in request.POST and request.POST['name']:
            name = request.POST['name']
        else:
            return ('/manager/updategroup/%d/?error=2' % int(info_id))

        # Format
        if 'format' in request.POST and request.POST['format']:
            format = request.POST['format']
        else:
            return ('/manager/updategroup/%d/?error=3' % int(info_id))

        group_code = int(code)
        group_name = name
        group_id = int(info_id)

        groups = list(Group.objects.filter(id=group_id))
        if not groups:
            return ('/manager/updategroup/%d/?error=4' % int(info_id))

        for p in groups:
            p.code = group_code
            p.name = group_name
            p.format = format
            p.save()

        return ('/manager/updategroup/%d' % group_id)

    # Tag
    def tag():

        # Code
        if 'code' in request.POST and request.POST['code']:
            code = request.POST['code']
        else:
            return ('/manager/updatetag/%d/?error=1' % int(info_id))

        # Name
        if 'name' in request.POST and request.POST['name']:
            name = request.POST['name']
        else:
            return ('/manager/updatetag/%d/?error=2' % int(info_id))

        tag_id = int(info_id)
        tag_code = int(code)
        tag_name = name

        tags = list(Tag.objects.filter(id=tag_id))
        if not tags:
            return ('/manager/updatetag/%d/?error=3' % int(info_id))

        for t in tags:
            t.code = tag_code
            t.name = tag_name
            t.save()

        return ('/manager/updatetag/%d' % tag_id)


    up = {
        "group": group,
        "tag": tag,
    }

    http = up[info_name]()
    return HttpResponseRedirect(http)


# Delete


def delete(request):

    if 'GInfo' in request.GET and request.GET['GInfo']:
        info_name = request.GET['GInfo']
    else:
        return HttpResponse("GInfo参数不存在!")

    # id
    if 'GID' in request.GET and request.GET['GID']:
        info_id = request.GET['GID']
    else:
        return HttpResponse("GID参数不存在!")


    # Group
    def group():

        group_id = int(info_id)

        groups = Group.objects.filter(id=group_id)
        if groups:
            groups.delete()

        return ('/manager/')

    # Tag
    def tag():

        tag_id = int(info_id)

        tags = Tag.objects.filter(id=tag_id)
        if tags:
            tags.delete()

        return ('/manager/tag/')


    Del = {
        "group": group,
        "tag": tag,
    }

    http = Del[info_name]()
    return HttpResponseRedirect(http)



