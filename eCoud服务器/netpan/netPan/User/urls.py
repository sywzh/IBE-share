#!/usr/bin/python
#! -*- coding: utf8 -*-

from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^register/$', views.RegisterHd),
    url(r'^login/$', views.LoginHd),
    url(r'^logout/$', views.LogoutHd),
    url(r'^changepw/$',views.ChangePw),
    url(r'^activate/([a-z0-9]+)/$',views.Activated),
    url(r'^addlist/$',views.addList),
    url(r'^viewaddlist/$',views.viewAddList),
    url(r'^modifylist/$',views.modifyList),
    url(r'^delList/$',views.delList),
    url(r'^viewlists/$',views.viewLists),
    url(r'^message/$',views.MessageHd),
    url(r'^noreadmsg/$',views.noReadMsg),
    url(r'^readmsg/$',views.readMsg),
    url(r'^historymsg/$',views.historyMsg),
)
