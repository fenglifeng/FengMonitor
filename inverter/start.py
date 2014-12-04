from sqldb import *
from YsLow10 import *
import time
import threading
from diesel import Service, Client, send, quickstart, quickstop
from diesel import until, call, log

def handle_echo(remote_addr):
	print "connected"
	#print remote_addr[0]
	tsqldb = sqldb()
	row = tsqldb.checkip(remote_addr[0])
	if(row != 0):
		#t = threading.Timer(5,ontime,[row[2]])
		#t.start()
		#test(sock)
		pass
	else:
		#print "no ip"
		pass
	while True:
		message = until('\r\n')
		send("you said: %s" % message)

def test(sock):
	sock.send("123")

def ontime(SINum):
	ys = YsLow10()
	#send(ys.createbuff(SINum))
	print "here"

class EchoClient(Client):
	@call
	def echo(self, message):
		send(message + '\r\n')
		back = until("\r\n")
		return back

log = log.name('echo-system')

def do_echos():
	try:
		client = EchoClient('localhost', 6000)
	except:
		quickstop()
		return
	t = time.time()
	for x in xrange(1):
		msg = "hello, world #%s!\r\n" % x
		echo_result = client.echo(msg)
		print echo_result
	log.info('5000 loops in {0:.2f}s', time.time() - t)
	while True:
		pass
	quickstop()

#quickstart(Service(handle_echo, port=6000),do_echos)
quickstart(do_echos)
#myserver = Service(handle_echo, port=8000)
