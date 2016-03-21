from django.conf.urls import patterns, include, url
from manager import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='administrator'),

    url(r'^tag', views.TagView.as_view(), name='tag'),

    url(r'^updatetag/(?P<tag_id>\d+)', views.TagUpdateView.as_view(), name='updatetag'),

    url(r'^updategroup/(?P<group_id>\d+)', views.GroupUpdateView.as_view(), name='updategroup'),

    url(r'^updategtt/(?P<gtt_id>\d+)', views.GTTUpdateView.as_view(), name='updategtt'),

    url(r'^updateinfo/(?P<gtt_id>\d+)/(?P<info_id>\d+)', views.TagInfoUpdateView.as_view(), name='updateinfo'),

    # ADD

    url(r'^add', views.create, name='add'),

    url(r'^gttadd', views.create_gtt, name='gttadd'),

    url(r'^infoadd', views.create_taginfo, name='infoadd'),

    # update

    url(r'^update', views.update, name='update'),

    url(r'^infoupdate', views.update_taginfo, name='infoupdate'),

    # delete

    url(r'^delete', views.delete, name='delete'),

    url(r'^gtdelete', views.del_gtt, name='gtdelete'),

    url(r'^infodelete', views.del_taginfo, name='infodelete'),

]