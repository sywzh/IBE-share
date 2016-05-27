#!/usr/bin/env python
#-*-coding:utf8-*-

from netPan.File.models import *
from netPan.File.views import gcFile,lastCapacity,isPdf,\
	isToPdf,isTxt,isDocument,fileWrite,fileRead,getFile
from netPan.filetype import fileType
from netPan.File.unoconv import output
from netPan.File.models import FileTable
from netPan.settings import mongoDB
from netPan.Log import folder_log,doc_log 
import base64


def Write(data):
	fp = open('test.txt','a')
	fp.write(data)
	fp.close()

def Read():
	f = open('test.txt','rb')
	buf = f.read()
	return buf

def HandleUpload(data):
	if data[0] == "#":
		buf = ''
	if data[-1] == ":":
		buf = buf + data[0:-1]
		return True,buf
	else:
		buf = buf + data
		return False,''

def storageFile(filename,user,fileurl,buf,doc_size,is_edit,key):
	try:
		capacity = lastCapacity(user,doc_size)
		if capacity<0:
			return ptcol.response('A')
		mongoDB.setCollection(user)
		id = mongoDB.creatFile(fileurl,buf)
		storage = FileTable(file_id = id,path = fileurl,name = filename,key = key,is_edit = is_edit)
		storage.save()
		doc_log(fileurl,name,'I')
		gcFile(buf)
		return response('E')
	except:
		gcFile(buf)
		return response('C')

def storageDocument(filename,user,fileurl,buf,key):
	try:
		mongoDB.setCollection(user)
		id = mongoDB.creatFile(fileurl,buf)
		storage = FileTable(file_id = id,path = fileurl,name = filename,key = key,is_edit = is_edit)
		storage.save()
		gcFile(buf)
		return True
	except:
		return False

def Upload(ptcol,path,name,size,data):
	print 'RECIEVE:',name,path,size,data
	Write(data)
	datas = Read()
	str_data = base64.decodestring(datas)
	print 'str_data:',str_data

	import os
	os.remove('test.txt')
	Write(str_data)

	'''
	write(str_data)
	'''


	ret,buf = HandleUpload(data)
	if ret:
		print 'fdfdsddf',buf
		user = ptcol.user
		file_type = fileType(buf)
		if isTxt(name):
			storageFile(name,user,path,buf,size,is_edit='1',key='0')
		elif isPdf(file_type):
			storageFile(name,user,path,buf,size,is_edit='0',key='0')
		elif isDocument(file_type):
			if storageDocument(name,user,path,buf,key='0'):
				fileWrite(buf)
				if output(name) == '0':
					name = name[:-3] + 'pdf'
					buff = fileRead(name)
					storageFile(name,user,path,buff,size,is_edit = '0',key='0')
				else:
					return ptcol.response('D')
			else:
				return ptcol.response('D')
		else:
			storageFile(name,user,path,buf,size,is_edit='0',key='0')

def Download(ptcol,path,filename):
	user = ptcol.user
	buf = getFile(path,user)

