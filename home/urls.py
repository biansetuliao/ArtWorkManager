from django.conf.urls import patterns, include, url
from home import views

urlpatterns = [

    url(r'^$', views.LoginView.as_view(), name='login'),

]