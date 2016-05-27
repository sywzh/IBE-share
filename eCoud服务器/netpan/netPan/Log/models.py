#!usr/bin/env python
#-*-coding:utf8-*-
from django.db import models
from datetime import datetime
from netPan.File.models import *
from django.contrib.auth.models import User

# Create your models here.

class ContentTable(models.Model):
	user = models.ForeignKey(User)
	path_name = models.CharField(max_length = 100)
	operate = models.CharField(max_length = 2)
	name = models.CharField(max_length = 60)
	time = models.DateTimeField(default = datetime.now)

	class Meta:
		ordering = ('-time',)

class DocumentTable(models.Model):
	user = models.ForeignKey(User)
	path_name = models.CharField(max_length = 100)
	operate = models.CharField(max_length = 2)
	name = models.CharField(max_length = 60)
	time = models.DateTimeField(default = datetime.now)

	class Meta:
		ordering = ('-time',)

class ShareLogTable(models.Model):

	OP_CHANGES = (
	    ('M','分享'),
	    ('N','被分享'),
	    ('Q','取消分享'),
	    ('O','修改权限')
	)

	user = models.ForeignKey(User)
	opname = models.CharField(max_length = 20)
	name = models.CharField(max_length = 60)
	operate = models.CharField(max_length = 1,choices = OP_CHANGES)
	time = models.DateTimeField(default = datetime.now)

	def Status(self):
		return dict(self.OP_CHANGES)[self.operate]

	class Meta:
		ordering = ('-time',)

class TrashLogTable(models.Model):
	user = models.ForeignKey(User)
	operate = models.CharField(max_length = 1)
	name = models.CharField(max_length = 60)
	time = models.DateTimeField(default = datetime.now)

	class Meta:
		ordering = ('-time',)


	


