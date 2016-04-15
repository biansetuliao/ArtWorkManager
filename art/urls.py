from django.conf.urls import patterns, include, url
from art import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='art'),

    url(r'^audit/$', views.ArtAuditView.as_view(), name='audit'),

    url(r'^upload/$', views.UploadTaskView.as_view(), name='upload'),

    url(r'^up_upload/$', views.UpdateUploadTaskView.as_view(), name='up_upload'),

    url(r'^pass/$', views.ArtPassView.as_view(), name='pass'),

    url(r'^faild/$', views.ArtFaildView.as_view(), name='faild'),

    url(r'^resource_upload/$', views.upload, name='resource_upload'),

]