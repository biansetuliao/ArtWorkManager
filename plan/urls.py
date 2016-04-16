from django.conf.urls import patterns, include, url
from plan import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='plan'),

    url(r'^gtt/$', views.GTTView.as_view(), name='gtt'),

    url(r'^search_bv/$', views.search_bv, name='search_bv'),

    url(r'^admin_plan/$', views.PlanAdminView.as_view(), name='admin_plan'),

    url(r'^audit_plan/$', views.PlanAuditView.as_view(), name='audit_plan'),

    url(r'^pass_task/$', views.PassTaskView.as_view(), name='pass_task'),

    url(r'^faild_task/$', views.FaildTaskView.as_view(), name='faild_task'),

    url(r'^task_audit/(?P<art_id>\d+)/$', views.AuditTaskView.as_view(), name='task_audit'),

    url(r'^create_task/$', views.create_task, name='create_task'),

    url(r'^del_task/$', views.del_task, name='del_task'),

    url(r'^download/$', views.download, name='download'),

]