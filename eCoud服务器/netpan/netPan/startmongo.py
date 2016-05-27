# -*- coding: utf-8 -*-
import pymongo
import re
class pyconnect(object):
	def __init__(self, host, port):
		try:
			self.conn = pymongo.Connection(host,port)
		except:
			print 'connect to %s:%s fail'%(host,port)
			exit(0)

	def use(self,dbname):
		self.db = self.conn[dbname]	

	def getDb(self):
		return self.db

	def close(self):
		self.conn.close()

	








	







		
