#!/usr/bin/env python
#-*-coding:utf8-*-

from ibe import GetIBE

get = GetIBE()

master = get.getMaster()
print 'master:',master

email = "821308407@qq.com"
getkey,getsecret = get.ibeEncode(email)

print 'getkey:',getkey
print 'getsecret:',getsecret

plaintext = get.ibeDecode(master,getsecret,email)
print 'plaintext:',plaintext
