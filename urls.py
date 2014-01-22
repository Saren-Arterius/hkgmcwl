from django.conf.urls import patterns, url

from hkgmcwl import views

urlpatterns = patterns('',
    url(r'^success/(?P<base64encoded>.+)$', views.success, name='success'),

    url(r'^password$', views.password, name='password'),
    url(r'^password/error/(?P<code>\d*)$', views.passwordError, name='passwordError'),
    url(r'^password/(?P<hkg_uid>\d+)/error/(?P<code>\d*)$', views.passwordValidateError, name='passwordValidateError'),
    url(r'^password/(?P<hkg_uid>\d+)/validate$', views.passwordValidateDo, name='passwordValidateDo'),
    url(r'^password/(?P<hkg_uid>\d+)$', views.passwordValidatePage, name='passwordValidatePage'),
    
    url(r'^$', views.index, name='index'),
    url(r'^error/(?P<code>\d*)$', views.error, name='error'),
    url(r'^(?P<base64encoded>.+)/error/(?P<code>\d*)$', views.validateError, name='validateError'),
    url(r'^(?P<base64encoded>.+)/validate$', views.validateDo, name='validateDo'),
    url(r'^(?P<base64encoded>.+)$', views.validatePage, name='validatePage'),
)

handler500 = views.errorHandler'