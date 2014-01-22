from django.conf.urls import patterns, url

from hkgmcwl import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^error/(?P<code>\d+)$', views.error, name='error'),
    url(r'^newuser/$', views.newuser, name='newuser'),
)