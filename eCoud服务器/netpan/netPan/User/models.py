#!/usr/bin/env python
#! -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    capacity = models.IntegerField(default = 50)
    activation_key = models.CharField(max_length = 40,default = '0')

    def __unicode__(self):
        return self.user.username

class AddressList(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length = 20)
    email = models.EmailField(blank = True)
    remarks = models.CharField(max_length = 50,null = True,blank = True)
class MessageList(models.Model):
    user = models.ForeignKey(User)
    targetname = models.CharField(max_length = 20)
    targetemail = models.EmailField(blank = True)
    time = models.DateTimeField(default = datetime.now)
    sending = models.BooleanField(default = True)

    def __unicode__(self):
        return self.targetname  

class MessageContent(models.Model):
    message = models.ForeignKey(MessageList)
    name = models.CharField(max_length = 20)
    targetname = models.CharField(max_length = 20)
    time = models.DateTimeField(default = datetime.now)
    content = models.CharField(max_length = 255)
    sending = models.BooleanField(default = True)

    def __unicode__(self):
        return self.content,self.name,self.targetname

def CreateUser(username,password,email,activation_key):
    user = User(username = username,email = email)
    user.set_password(password)
    user.email = email
    user.is_staff = False
    user.is_active = False
    user.save()

    profile = UserProfile(user = user)
    profile.capacity = 50*1024*1024
    profile.activation_key = activation_key
    profile.save()
    return user,profile
