from django.conf.urls import patterns, url

from hkgmcwl import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^error/(?P<code>\d*)$', views.error, name='error'),
    url(r'^success/(?P<base64encoded>.+)$', views.validateSuccess, name='validateSucess'),
    url(r'^(?P<base64encoded>.+)/error/(?P<code>\d*)$', views.validateError, name='validateError'),
    url(r'^(?P<base64encoded>.+)/validate$', views.validateDo, name='validateDo'),
    url(r'^(?P<base64encoded>.+)$', views.validatePage, name='validatePage'),
)