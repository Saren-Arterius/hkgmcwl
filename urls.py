from django.conf.urls import patterns, url

from hkgmcwl import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^error/(?P<code>\d*)$', views.error, name='error'),
    url(r'^(?P<base64encoded>.+)/confirm$', views.confirmDo, name='confirmDo'),
    url(r'^(?P<base64encoded>.+)/error$', views.confirmError, name='confirmError'),
    url(r'^(?P<base64encoded>.+)/success$', views.confirmSuccess, name='confirmSucess'),
    url(r'^(?P<base64encoded>.+)$', views.confirmPage, name='confirmPage'),
)