from django.conf.urls import patterns, include, url
from plan import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='plan'),

    url(r'^gtt/$', views.GTTView.as_view(), name='gtt'),

    url(r'^search_bv/$', views.search_bv, name='search_bv'),

    url(r'^admin_plan/$', views.PlanAdminView.as_view(), name='admin_plan'),

    url(r'^audit_plan/$', views.PlanAuditView.as_view(), name='audit_plan'),

    url(r'^yaudit_plan/$', views.YAuditTaskView.as_view(), name='yaudit_plan'),

    url(r'^task_audit/$', views.AuditTaskView.as_view(), name='task_audit'),

]