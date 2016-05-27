# -*- coding: utf-8 -*-
import pymongo
import re
import bson
class pyoperate(object):

	def __init__(self, db):
		self.db = db

	def setCollection(self,collection):
		if not self.db:
			print 'don\'t assign database'
			exit(0)
		else:
			self.coll = self.db[collection]	
			return 'success'

	def creatFile(self,path,data):
		try:
			path = ''.join(path.split('.'))
			data = bson.Binary(data)
			p = re.compile(r'\$+')
			List = p.split(path)
			Len = len(List)
			for i in range(0,Len-1):
				strtemp = List[i]
				self.coll = self.coll[strtemp]
			self.coll.insert({List[Len-1]:data})
			result = self.coll.find_one({List[Len-1]:data})
			return result['_id']
		except:
			return 'error'

	def getFileData(self,path,id):
		try:
			id = bson.objectid.ObjectId(id)
			path = ''.join(path.split('.'))
			p = re.compile(r'\$+')
			List = p.split(path)
			Len = len(List)
			for i in range(0,Len-1):
				strtemp = List[i]
				self.coll = self.coll[strtemp]
			result = self.coll.find_one({'_id':id})
			return result[List[Len-1]]
		except:
			return 'error'
	
	def creatDir(self,path):
		try:
			path = ''.join(path.split('.'))
			p = re.compile(r'\$+')
			List = p.split(path)
			Len = len(List)
			for i in range(0,Len):
				strtemp = List[i]
				self.coll = self.coll[strtemp]
			return 'success'
		except:
			return 'error'

	def deleteFile(self,path,id):
		try:
			id = bson.objectid.ObjectId(id)
			path = ''.join(path.split('.'))
			p = re.compile(r'\$+')
			List = p.split(path)
			Len = len(List)
			for i in range(0,Len):
				strtemp = List[i]
				self.coll = self.coll[strtemp]
			self.coll.remove({'_id':id})
			return 'success'
		except:
			return 'error'

	def deleteDir(self,path):
		try:
			path = ''.join(path.split('.'))
			p = re.compile(r'\$+')
			List = p.split(path)
			Len = len(List)
			for i in range(0,Len):
				strtemp = List[i]
				self.collpro = self.coll
				self.coll = self.coll[strtemp]
			self.coll.remove()
			self.coll = self.collpro
			return 'success'
		except:
			return 'error'

	def update(self,data,setdata):
		if type(data) is not dict or type(setdata) is not dict:
			print 'the type of update and data isn\'t dict'
			exit(0)
		self.coll.update(data,{'$set':setdata})

	def addMessage(self,path,message):
		try:
			path = ''.join(path.split('.'))
			p = re.compile(r'\$+')
			List = p.split(path)
			Len = len(List)
			for i in range(0,Len):
				strtemp = List[i]
				self.coll = self.coll[strtemp]
			num = self.coll.find().count()
			num = num + 1
			self.coll.insert({num:message})
			return num
		except:
			return 'error'
	def returnMessage(self,path):
		try:
			path = ''.join(path.split('.'))
			p = re.compile(r'\$+')
			List = p.split(path)
			Len = len(List)
			for i in range(0,Len):
				strtemp = List[i]
				self.coll = self.coll[strtemp]
			result = self.coll.find()
			num = self.coll.find()
			List = []
			for x in result:
				List.append(x[num])
				num = num - 1
			return List
		except:
			return 'error'
