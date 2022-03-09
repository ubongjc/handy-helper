from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^jobs/new/$', views.new_job, name='new_job'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^jobs/(?P<id>\d+)/$', views.view_job, name='view_job'),
    url(r'^jobs/edit/(?P<id>\d+)/$', views.edit_job, name='edit_job'),
    url(r'^dashboard/jobs/remove/$', views.remove_job, name='remove_job'),
    url(r'^dashboard/jobs/giveup/$', views.giveup_job, name='giveup_job'),
    url(r'^process/signup/$', views.process_signup, name='process_signup'),
    url(r'^process/signin/$', views.process_signin, name='process_signin'),
    url(r'^jobs/user/add/(?P<id>\d+)/$', views.add_user_job, name='add_user_job'),
    url(r'^jobs/giveup/(?P<id>\d+)/$', views.giveup_the_job, name='giveup_the_job'),
    url(r'^dashboard/user/jobs/add/$', views.add_job_to_user, name='add_job_to_user'),
    url(r'^dashboard/jobs/new/process/$', views.process_new_job, name='process_new_job'),
    url(r'^process/jobs/edit/(?P<id>\d+)/$', views.process_job_edit, name='process_job_edit'),
]