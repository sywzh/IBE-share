#!/usr/bin/python
#-*coding:utf-8*-
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

def lrender(tpl = None):
    def func(f):
        def infunc(req, *args, **kwargs):
            r = f(req, *args, **kwargs)
            if isinstance(r, HttpResponse):
                return r
            elif tpl and 'tpl' not in r:
                return render_to_response(tpl, RequestContext(req, r))
            else:
                return render_to_response(r.pop('tpl'), RequestContext(req, r))
        return infunc
    return func

def ensure_staff(func):
    def infunc(request,*argv,**kwargv):
        if not request.user.is_staff:
            raise Http404
        else:
            return func(request,*argv,**kwargv)
    return infunc

