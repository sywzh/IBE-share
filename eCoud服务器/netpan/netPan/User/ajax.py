#!/usr/bin/env python
#-*-coding:utf8-*-

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from netPan.decorators import lrender
from django.http import HttpResponseRedirect

@dajaxice_register
def RegisterHd(request,register):
	'''
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('netPan.index.IndexHd'))
	'''
#@lrender('User/login.html')
@dajaxice_register
def LoginHd(request,login):
	print login
	return simplejson.dumps({'message':'your message is %s!' % login})