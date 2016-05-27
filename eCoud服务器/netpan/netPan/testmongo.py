#!/usr/bin/env python
#-*-coding:utf8-*-

from startmongo import pyconnect
from mongo import pyoperate
import bson
from django.utils import simplejson 

connect = pyconnect('localhost',27017)
connect.use('netPandb')
user = pyoperate(connect.getDb())

user.setCollection('test')
id = user.creatFile('A$z','this is test')
print id

pid = id.binary
print type(id.binary)
pid = bson.objectid.ObjectId(pid)
print 'pid',type(pid)

user.setCollection('test')
buf  = user.getFileData('A$z',id)
print buf

fp = open('1.pdf','rb')
buf = bson.Binary(fp.read())
fp.close()
fileurl = 'A$3.pdf'
fileurl = ''.join(fileurl.split('.'))
user.setCollection('testtest')
id = user.creatFile(fileurl,buf)
print id

user.setCollection('testtest')
buf = user.getFileData('A$3.pdf',id)
print type(buf)
print dir(buf)
'''
buf = str(buf)
print type(buf)
'''

pf = open('4.pdf','wb')
pf.write(buf)
pf.close()


