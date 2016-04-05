from django.contrib import admin
from home.models import *


class GroupToTagInline(admin.TabularInline):
    model = GroupToTag
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'format', )
    inlines = [GroupToTagInline]


class TagAdmin(admin.ModelAdmin):
    list_display = ("code", "name", )


class TagInfoAdmin(admin.ModelAdmin):
    list_display = ('get_group', 'get_tag', 'code', 'name', )

    def get_group(self, obj):
        return obj.group.name
    get_group.short_description = 'Group'
    get_group.admin_order_field = 'Group__name'

    def get_tag(self, obj):
        return obj.tag.name
    get_tag.short_description = 'Tag'
    get_tag.admin_order_field = 'tag__name'


class ArtInfoInline(admin.TabularInline):
    model = ArtInfo
    extra = 1


class ArtAdmin(admin.ModelAdmin):
    list_display = ('get_group', 'version', 'upload_time', 'is_pass', )
    inlines = [ArtInfoInline]

    def get_group(self, obj):
        return obj.group.name
    get_group.short_description = 'Group'
    get_group.admin_order_field = 'Group__name'


admin.site.register(Group, GroupAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagInfo, TagInfoAdmin)
admin.site.register(Art, ArtAdmin)