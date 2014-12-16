import SocketServer 
from YsLow10 import *
from sqldb import *
from Pysettimer import *
from sip import *
from crc16 import *

HOST = '' 
PORT = 6000
ADDR = (HOST,PORT)

class RequerstHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		#set ip
		#print "hello world"
		#self.request.send("welcome")
		IP = self.client_address[0]
		print IP
		tsqldb = sqldb()
		row = tsqldb.checkip(IP)
		if(row != 0):
			SINum = row[2]
			ys = YsLow10()
			buff = ys.createbuff(int(SINum))
			self.mysend = Pysettimer(self.test,(buff),timeout =5,is_loop=True)	
			self.mysend.start()
		else:
			self.request.close()
			return
		try:
			si = sip()
			while True:
				recdata = self.request.recv(128)
				#recdatat = 
				if(len(recdata)>5):
					#self.request.send()
					crc = crc16()
					if crc.calcrc(recdata) ==1:
						continue
					si.readdata(recdata)
					#print si.SINum
					#print si.Hz
					tsqldb = sqldb()
					tsqldb.SaveTempParameters(si)
					continue
				else:
					break
				pass
			self.request.close()
			self.mysend.stop()
		except KeyboardInterrupt:
			try:
				mysend.stop()
			except:
				pass
	def test(self,buff):
		try:
			self.request.send(bytearray(buff))
		except:
			print "error"
			self.mysend.stop()
			return

def OnTimeSave(args):
	mtime = time.strftime('%H:%M:%S',time.localtime(time.time()))
	minute = mtime[-5:-3]
	if int(minute)%12 == 0:
		mysql = sqldb()
		rows = mysql.getAllSinum()
		for row in rows:
			sinum = row[0]			
			mysql.SaveParameters(sinum)
		mysql.deletetemp()
	return

SocketServer.ThreadingTCPServer.allow_reuse_address = True
#监控进程
tcpserver = SocketServer.ThreadingTCPServer(ADDR,RequerstHandler)
#定时存储
ontime = Pysettimer(OnTimeSave,timeout=60,is_loop=True)	
ontime.start()
tcpserver.serve_forever()
