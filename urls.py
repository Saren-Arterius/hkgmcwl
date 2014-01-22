from django.conf.urls import patterns, url

from hkgmcwl import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^error/(?P<code>\d*)$', views.error, name='error'),
    url(r'^confirm/$', views.confirmPage, name='confirmPage'),
    url(r'^confirm/error/(?P<code>\d*)$', views.confirmError, name='confirmError'),
    url(r'^confirm/(?P<base64encoded>.+)$', views.confirm, name='confirm'),
)