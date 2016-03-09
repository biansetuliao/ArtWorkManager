from django.conf.urls import patterns, include, url
from manager import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='administrator'),

    url(r'^tag', views.TagView.as_view(), name='tag'),

    # ADD

    url(r'^add', views.create, name='add'),



]