from django.conf.urls import patterns, include, url
from plan import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='plan'),

]