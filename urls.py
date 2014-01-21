from django.conf.urls import patterns, url

from hkgmcwl import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^version/$', views.newuser, name='newuser'),
)