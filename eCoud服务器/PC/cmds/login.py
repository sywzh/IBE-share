#!/usr/bin/env python
#-*-coding:utf8-*-

from django.contrib.auth.models import User
from netPan.User.models import *

def Login(ptcol,username,password):
	try:
		assert(ptcol.user == None)
		ptcol.user = User.objects.get(username = username)
		assert ptcol.user.check_password(password)
	except User.DoesNotExist:
		return ptcol.response('failure\x00')#username error
	except AssertionError:
		return ptcol.response('failure\x00')#password error
	ptcol.response('ok\x00')

def Register(ptcol,username,email,password):
	if User.objects.filter(username = username).count() > 0:
		return ptcol.response('failure\x00')#username has registered
	if User.objects.filter(email = email).count() > 0:
		return ptcol.response('failure\x00') #email has used
	try:
		user,profile = CreateUser(username,password,email)
	except:
		return ptcol.response('failure\x00')
	return ptcol.response('ok\x00')

