
#!/usr/bin/env python
#-*-coding:utf8-*-

from twisted.protocols.basic import LineReceiver
from cmds import CMDS
import struct

'''
def write(buf):
	fp = open('1.txt','a+')
	fp.write(buf)
	fp.close()
'''

class NetpanProtocol(LineReceiver):
	def connectionMade(self):
		self.delimiter = '\n'
		self.arg_delimiter = ' '
		self.user = None
	def response(self,data,ok = True):
		self.transport.write('#' + struct.pack('<?I',ok,len(data)) + data)
	def lineReceived(self,line):
		#write(line)
		cmds = line.split(self.arg_delimiter)
		print 'cmds:',cmds	
		cmd,args = cmds[0],cmds[1:]
		print 'cmd:',cmd
		if cmd not in CMDS:
			self.sendLine('no such command')
			return self.transport.loseConnection()
		cmd_func,args_len,login_required = CMDS[cmd]
		if len(args) != args_len:
			self.sendLine('command arguments wrong')
			return self.transport.loseConnection()
		if login_required and not self.user:
			return self.sendLine('login required')
		try:
			cmd_func(self,*args)
		except:
			self.sendLine('server error')
			self.transport.loseConnection()