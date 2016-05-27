#!/usr/bin/env python
#-*-coding:utf8-*-

from ctypes import *

class GetIBE(object):

	def __init__(self):
		self.libc = CDLL("./ibe_test.so")

	def getMaster(self):
		Setup = self.libc.Setup
		self.masterkey = create_string_buffer(40)
		Setup(self.masterkey)
		return self.masterkey.value

	def ibeEncode(self,email):
		getCipher = self.libc.getCipher
		self.getkey = create_string_buffer(40)
		self.getsecret = create_string_buffer(220)
		self.id = c_char_p(email)
		getCipher(self.getkey,self.getsecret,self.id)
		count = 0
		while count < 5:
			if self.getsecret.value[-1:] != '=':
				getCipher(self.getkey,self.getsecret,self.id)
				count  = count + 1
				if count == 5:
					return False,'',''
			else:
				break
		
		return True,self.getkey.value,self.getsecret.value

	def ibeDecode(self,masterkey,getsecret,email):
		getDecode = self.libc.getDecode
		self.masterkey = c_char_p(masterkey)
		self.getsecret = c_char_p(getsecret)
		self.id = c_char_p(email)
		self.plaintext = create_string_buffer(40)
		getDecode(self.masterkey,self.getsecret,self.id,self.plaintext)
		return self.plaintext.value