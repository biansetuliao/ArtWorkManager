from django.conf.urls import patterns, include, url
from art import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='art'),

]