#!/usr/bin/env python
#!-*-coding:utf8-*-

from django.core.management import setup_environ
import settings

setup_environ(settings)
import os
from django.db import connection
cur = connection.cursor()
dbname = settings.DATABASES['default']['NAME']
try:
	cur.execute('drop database %s;' % dbname)
except:
	pass
cur.execute('create database %s CHARACTER SET utf8;' %dbname)
cur.execute('use %s' %dbname)
cur.close()

if os.system('echo "no" | python ../manage.py syncdb'):
	exit(-1)

from User.models import *
u,p = CreateUser('testtest','123456','821308407@qq.com','0')
u.is_staff = True
u.is_superuser = True
u.is_active = True
u.save()

from netPan.File.models import IBEMaster
from ibe import GetIBE
get = GetIBE()
try:
	master = get.getMaster()
except:
	print 'generate master error!'
try:
	op = IBEMaster(master = master)
	op.save()
	os.system('cp params.txt ../')
except:
	print 'get master error!'

from netPan.File.models import *
from netPan.settings import mongoDB 
import gc
import bson
from netPan.Log import *
from netPan.File.aes import mycrypt

fp = open('1.pdf','rb')
buf = fp.read()
fp.close()

ret,getkey,getsecret = get.ibeEncode(u.email)
aeskey = getkey + '!@#$'
op = mycrypt(aeskey)
buf = op.myencrypt(buf)

fileurl = 'testtest$1.pdf'
mongoDB.setCollection(u.username)
id = mongoDB.creatFile(fileurl,buf)
print 'id',id
storage = FileTable(file_id = id,user_id = u.id,path = '$',name='1.pdf',key = getsecret,is_edit='0',is_folder = '0',is_browser = '1',typefile = '0')
storage.save()
doc_log('$','1.pdf','A',u.id)
del buf
gc.collect()

sid = mongoDB.creatDir('testtest$folder')
print sid
storage = FileTable(file_id = sid,user_id = u.id,path = '$',name='folder',key = '0',is_edit='0',is_folder = '1',is_browser = '0')
storage.save()

mongoDB.setCollection(u.username)
buf = mongoDB.getFileData(fileurl,id)
ibekey = get.ibeDecode(master,getsecret,u.email)
keyaes = ibekey + '!@#$'
opt = mycrypt(keyaes)
buf = opt.mydecrypt(buf).rstrip()

pf = open('3.pdf','wb')
pf.write(buf)
pf.close()
del buf
gc.collect()

from django.contrib.sites.models import Site

site = Site.objects.get_current()
site.domain = settings.SET_DOMAIN
site.save()

from File.unoconv import output
import time
ret = output("2.doc")
print ret
while ret != 0:
	time.sleep(30)
	print '正在开启转换模块，请稍候。。。'
	ret = output("2.doc")
	print ret
print '转换模块开启成功...'

