from django.conf.urls import patterns, include, url
from login import views

urlpatterns = [
    # ex: /sign_in/
    url(r'^sign_in/$', views.sign_in, name='sign_in'),

    # ex: /sign_out/
    url(r'^sign_out/$', views.sign_out, name='sign_out'),

    # ex: /sign_success/
    url(r'^menu/$', views.MenuViews.as_view(), name='menu'),
]