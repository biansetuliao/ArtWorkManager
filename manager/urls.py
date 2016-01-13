from django.conf.urls import patterns, include, url
from manager import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='administrator'),

]