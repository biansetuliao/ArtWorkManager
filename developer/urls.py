from django.conf.urls import patterns, include, url
from developer import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='developer'),

    url(r'^gtt/$', views.GTTView.as_view(), name='gtt'),

    url(r'^search/$', views.search_image, name='search'),

]