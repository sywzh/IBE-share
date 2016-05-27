#!/usr/bin/python
#! -*- coding: utf8 -*-

from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^upload/$',views.uploadifyScript),
    url(r'^share/$',views.shareFile),
    url(r'^delete/$',views.deleteFile),
    url(r'^search/$',views.searchFile),
    url(r'^coordination/$',views.coordinationFile),
    url(r'^coordinationto/$',views.coordinationToFile),
    url(r'^sharein/$',views.shareInFile),
    url(r'^shareout/$',views.shareOutFile),
    url(r'^download/(\w+)/$',views.downLoad),
    url(r'^delfile/$',views.delFile),
    url(r'^refile/$',views.resumeFile),
    url(r'^redelfile/$',views.reDelFile),
    url(r'^browser/(\w+)/$',views.browserFile),
    url(r'^viewfile/$',views.viewFile),
    url(r'^myfile/$',views.myFile),
    url(r'^myshare/$',views.Share),
    url(r'^reviewmyshare/$',views.reViewCancelShare),
    url(r'^newfolder/$',views.newFolder),
    url(r'^changeshare/$',views.changeShareO),
    url(r'^sharedownload/(\w+)/$',views.shareDownload),
    url(r'^cancelshare/$',views.cancelShare),
    url(r'^browserbuf/$',views.browserFuf),
    url(r'^pubshare/$',views.pubShare),
    url(r'^mypubshare/$',views.myPubShare),
    url(r'^cancelpubshare/$',views.cancelPubShare),
    url(r'^modifypubshare/$',views.modifyPubShare),
    url(r'^searchfile/$',views.Search),
    url(r'^viewfolder/$',views.viewFolder),
    )
