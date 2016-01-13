from django.conf.urls import patterns, include, url
from developer import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='developer'),

]