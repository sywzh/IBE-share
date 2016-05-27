#!usr/bin/env python
#-*-coding:utf8-*-

def init():
	import os,sys
	print sys.path.append('../'+os.path.join(os.path.dirname(__file__),'netpan'))
	from django.core.management import setup_environ
	import netPan.settings
	setup_environ(netPan.settings)

init()

from twisted.internet import ssl,reactor
from twisted.internet.protocol import Factory
from protocol import NetpanProtocol
import config
from twisted.python import log

class NetpanFactory(Factory):
	protocol = NetpanProtocol

if __name__ == '__main__':
	import sys
	log.startLogging(sys.stdout)
	factory = NetpanFactory()
	context = ssl.DefaultOpenSSLContextFactory(config.KEY_FILE,config.CERT_FILE)
	reactor.listenSSL(config.LISTEN_PORT,factory,context)
	reactor.run()