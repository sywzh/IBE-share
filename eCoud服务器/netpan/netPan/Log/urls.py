#!/usr/bin/python
#! -*- coding: utf8 -*-

from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
	url(r'^filelog/$',views.fileLog),
	url(r'^sharelog/$',views.shareLog),
	url(r'^trashlog/$',views.trashLog),
	)