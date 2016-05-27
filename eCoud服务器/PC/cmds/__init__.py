#!/usr/bin/env python
#-*-coding:utf8-*-

import login
import files

def bye(ptcol):
	ptcol.transport.loseConnection()

CMDS = {
	'bye':(bye,0,False),
	'login':(login.Login,2,False),
	'logout':(bye,0,False),
	'register':(login.Register,3,False),
	'UploadFile':(files.Upload,4,True),
}