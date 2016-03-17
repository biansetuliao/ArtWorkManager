from django.conf.urls import patterns, include, url
from manager import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='administrator'),

    url(r'^tag', views.TagView.as_view(), name='tag'),

    url(r'^updatetag/(?P<tag_id>\d+)', views.TagUpdateView.as_view(), name='updatetag'),

    url(r'^updategroup/(?P<group_id>\d+)', views.GroupUpdateView.as_view(), name='updategroup'),

    # ADD

    url(r'^add', views.create, name='add'),

    # update

    url(r'^update', views.update, name='update'),

    # delete

    url(r'^delete', views.delete, name='delete'),

]