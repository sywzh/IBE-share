#!/bin/usr/env python
#-*-coding:utf8-*-

from django.conf.urls import patterns, include, url



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'netPan.views.home', name='home'),
    # url(r'^netPan/', include('netPan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','netPan.User.views.LogoHd'),
    url(r'^index/$','netPan.index.IndexHd'),
    url(r'^user/',include('netPan.User.urls')),
    url(r'^file/',include('netPan.File.urls')),
    url(r'^log/',include('netPan.Log.urls')),
    #url(r'^accounts/password/change/$','django.contrib.auth.views.password_change',{'template_name':'User/password_change.html'}),
    #url(r'^accounts/password/change/done/$','django.contrib.auth.views.password_change_done',{'template_name':'User/password_change_success.html'}),
    url(r'^accounts/password/reset/$','django.contrib.auth.views.password_reset',{'template_name':'User/password_reset.html'}),
    url(r'^accounts/password/reset/done/$','django.contrib.auth.views.password_reset_done',{'template_name':'User/password_reset_done.html'}),
    url(r'^accounts/password/pw_reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','django.contrib.auth.views.password_reset_confirm',{'template_name':'User/password_reset_confirm.html'}),
    url(r'^accounts/password/done/$','django.contrib.auth.views.password_reset_complete',{'template_name':'User/password_reset_complete.html'}),


    url(r'^test/$','netPan.ajax.multiply'),

)
