#!/usr/bin/env python
#! -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from netPan.decorators import lrender
from django.contrib.auth import login, logout
from models import *
from django.utils import simplejson
from django.contrib.auth import authenticate
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import Context,loader
import random
from django.utils.hashcompat import sha_constructor
from netPan import settings
from django.core.mail import EmailMultiAlternatives  
from django.core import serializers
from django.contrib.sites.models import Site

@csrf_exempt
def RegisterHd(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	username = request.POST.get("username")
	password = request.POST.get("password")
	email = request.POST.get("email")
	if User.objects.filter(username = username).count()>0:
		return HttpResponse(simplejson.dumps({'message':'A'}))
	if User.objects.filter(email = email).count()>0:
		return HttpResponse(simplejson.dumps({'message':'B'}))
	activation_key = reset_activation_key(email)
	user,profile = CreateUser(username,password,email,activation_key)
	if SendEmail(user,activation_key):
		return HttpResponse(simplejson.dumps({'message':'I'}))
	else:
		p = UserProfile.objects.get(user__username = username)
		p.delete()
		p.save()
		return HttpResponse(simplejson.dumps({'message':'J'}))

@csrf_exempt
def LoginHd(request):
	if request.method != 'POST' or not request.is_ajax():
		raise Http404
	content_type = 'application/json;charset=utf-8'
	username = request.POST.get("username")
	password = request.POST.get("password")
	user = authenticate(username=username, password=password)
	if not user:
		return HttpResponse(simplejson.dumps({'message':'C'}),content_type = content_type)
	if not user.is_active:
		return HttpResponse(simplejson.dumps({'message':'H'}))
	login(request,user)
	return HttpResponse(simplejson.dumps({'message':'D'}))

def LogoutHd(request):
	logout(request)
	return HttpResponseRedirect(reverse('netPan.User.views.LogoHd'))

@lrender('logoPage.html')
@csrf_exempt
def LogoHd(request):
	return {}


@login_required
@lrender('User/password_change.html')
@csrf_exempt
def ChangePw(request):
	if request.method == 'POST' or request.is_ajax():
		username = request.user
		old_password = request.POST.get("old_password")
		user = authenticate(username = username,password = old_password)
		if user is not None and user.is_active:
			new_password = request.POST.get("new_password")
			user.set_password(new_password)
			user.save()
			return HttpResponse(simplejson.dumps({'message':'G'}))
		else:
			return HttpResponse(simplejson.dumps({'message':'F'}))
	return {}

def SendEmail(user,code):
	try:
		site = Site.objects.get_current()
		domain = site.domain
		email = user.email
		html_content = loader.render_to_string('User/send_email.html',{'email_code':code,'user':user,'domain':domain})
		subject,form_email,to = settings.SUBJECT,settings.EMAIL_HOST_USER,email
		text_content = 'netPan'
		msg = EmailMultiAlternatives(subject,text_content,form_email,[to])
		msg.attach_alternative(html_content,'text/html')
		msg.send()
		return True
	except:
		return False
def reset_activation_key(email):
	salt = sha_constructor(str(random.random())).hexdigest()[:5]
	if isinstance(email,unicode):
		email = email.encode('utf-8')
	activation_key = sha_constructor(salt + email).hexdigest()
	return activation_key

@csrf_exempt
@lrender('User/activate.html')
def Activated(request,code):
	try:
		profile = UserProfile.objects.get(activation_key = code)
	except UserProfile.DoesNotExist:
		return {'message':'K'}
	try:
		user = User.objects.get(id = profile.user_id)
	except User.DoesNotExist:
		return {'message':'N'}
	if user.is_active:
		return {'message':'L'}
	else:
		user.is_active = True
		user.save()
	return{'message':'M'}

def storageList(email,id,username,remarks):
	try:
		storage = AddressList(email = email,user_id = id,username = username,remarks = remarks)
		storage.save()
		return True
	except:
		return False

def Lists(user,email):
	try:
		if AddressList.objects.filter(user__username = user,email = email).count() == 1:
			return True
	except:
		return False

@login_required
@csrf_exempt
def addList(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	email = request.POST.get("address")
	remarks = request.POST.get("remark")
	if Lists(request.user.username,email):
		return HttpResponse(simplejson.dumps({'message':'U'}))
	try:
		user = User.objects.get(email = email)
	except User.DoesNotExist:
		return HttpResponse(simplejson.dumps({'message':'N'}))
	if storageList(email,request.user.id,user.username,remarks):
		return HttpResponse(simplejson.dumps({'message':'O'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'P'}))

@csrf_exempt
@lrender('User/addressLists.html')
@login_required
def viewAddList(request):
	try:
		users = AddressList.objects.filter(user__username = request.user)
		return {'users':users}
	except:
		return {'users':'R'}

@csrf_exempt
@login_required
def viewLists(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	lists = AddressList.objects.filter(user__username = request.user)
	all_lists = serializers.serialize("json",lists)
	return HttpResponse(simplejson.dumps({'all_lists':all_lists}))

def modifyStorage(uid,remark):
	try:
		user = AddressList.objects.get(id = uid)
		user.remarks = remark
		user.save()
		return True
	except:
		return False
@csrf_exempt
@login_required
def modifyList(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	uid = request.POST.get("id")
	remark = request.POST.get("remark")
	if modifyStorage(uid,remark):
		return HttpResponse(simplejson.dumps({'message':'V'}))
	else:
		return HttpResponse(simplejson.dumps({'message':'W'}))

@csrf_exempt
@login_required
def delList(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	uid = request.POST.get("id")
	try:
		user = AddressList.objects.filter(id = uid)
		user.delete()
		return HttpResponse(simplejson.dumps({'message':'S'}))
	except:
		return HttpResponse(simplejson.dumps({'message':'T'}))

@login_required
@lrender('User/msg.html')
def MessageHd(request):
	try:
		messages = MessageList.objects.filter(user__username = request.user,sending = False)
		return {'messages':'messages'}
	except:
		raise Http404

@login_required
@csrf_exempt
def noReadMsg(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	try:
		messages = MessageList.objects.filter(user__username = request.user,sending = False)
		all_messages = serializers.serialize("json",messages)
		return HttpResponse(simplejson.dumps({'all_messages':all_messages}))
	except:
		raise Http404

@login_required
@csrf_exempt
def readMsg(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	try:
		messages = MessageList.objects.filter(user__username = request.user,sending = True)
		all_messages = serializers.serialize("json",messages)
		return HttpResponse(simplejson.dumps({'all_messages':all_messages}))
	except:
		raise Http404

@login_required
@csrf_exempt
def historyMsg(request):
	if not request.is_ajax() or request.method != 'POST':
		raise Http404
	id = request.POST.get("id")
	try:
		messages = MessageContent.objects.filter(message_id = id)
		all_messages = serializers.serialize("json",messages)
		return HttpResponse(simplejson.dumps({'all_messages':all_messages}))
	except:
		raise Http404

	