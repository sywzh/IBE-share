#!/usr/bin/env python
#-*-coding:utf8-*-

from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django_socketio import events
from models import MessageContent

@events.on_message(channel="^user-")
def message(request,socket,context,message):
	if message["action"] == "message":
		message["message"] = strip_tags(message["message"])
		message["name"] = request.user.username
		socket.send_and_broadcast_channel(message)
	

@events.on_finish(channel = "^user-")
def finish(request,socket,context):
	try:
		user = context["user"]
	except KeyError:
		return 
	left = {"action":"leave","name":user.name,"id":user.id}
	socket.broadcast_channel(left)
	