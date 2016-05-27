#!usr/bin/env python
#-*-coding:utf8-*-
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class FileTable(models.Model):
	file_id = models.CharField(max_length = 24)
	user = models.ForeignKey(User)
	path = models.CharField(max_length = 100)
	name = models.CharField(max_length = 60)
	key = models.CharField(max_length = 220,default = '0')
	is_folder = models.CharField(max_length = 1,default = '0')
	is_edit = models.CharField(max_length = 1,default = '0')
	is_browser = models.CharField(max_length = 1,default = '0')
	is_delete = models.CharField(max_length = 1,default = '0')
	upload_time = models.DateTimeField(default = datetime.now)
	typefile = models.CharField(max_length = 1,default = '4')

	class Meta:
		ordering = ('-upload_time',)

	def __unicode__(self):
		return self.path,self.name

class MyShareTable(models.Model):
	user = models.ForeignKey(User)
	file = models.ForeignKey(FileTable)
	time = models.DateTimeField(default = datetime.now)
	share_who = models.CharField(max_length = 20)
	is_edit = models.CharField(max_length = 1,default = '0')
	is_download = models.CharField(max_length = 1,default = '0')

	class Meta:
		ordering = ('-time',)

	def __unicode__(self):
		return self.share_who,self.user

class ShareMeTable(models.Model):
	user = models.ForeignKey(User)
	file = models.ForeignKey(FileTable)
	time = models.DateTimeField(default = datetime.now)
	who_share = models.CharField(max_length = 20)
	is_edit = models.CharField(max_length = 1,default = '0')
	is_download = models.CharField(max_length = 1,default = '0')

	class Meta:
		ordering = ('-time',)

	def __unicode__(self):
		return self.who_share,self.user

class ShareTable(models.Model):
	file = models.ForeignKey(FileTable)
	name = models.CharField(max_length = 60)
	time = models.DateTimeField(default = datetime.now)
	is_download = models.CharField(max_length = 1,default = '0')

	class Meta:
		ordering = ('-time',)

class IBEMaster(models.Model):
	master = models.CharField(max_length = 29,default = '0')

class ConvertTable(models.Model):
	file = models.ForeignKey(FileTable)
	fid = models.CharField(max_length = 24)


