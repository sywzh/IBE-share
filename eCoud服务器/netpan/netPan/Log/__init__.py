#!/usr/bin/env python
#-*-coding:utf8-*-

from models import *

def folder_log(pathname,name,operate,userid):
	log = ContentTable()
	log.user_id = userid
	log.path_name = pathname
	log.operate = operate
	log.name = name
	log.save()

def doc_log(pathname,name,operate,userid):
	log = DocumentTable(user_id = userid,path_name = pathname,operate = operate,name = name)
	log.save()

def shareLog(userid,opname,name,operate):
	log = ShareLogTable(user_id = userid,opname = opname,name = name,operate = operate)
	log.save()

def trashLog(userid,name,operate):
	log = TrashLogTable(user_id = userid,name = name,operate = operate)
	log.save()


