from crc16 import *

class YsLow10:
	crc = crc16()
	def __init__(self):
		pass
	def createbuff(self,SINum):
		array = [SINum,0x03,0xe4,0x21]
		return self.crc.createarray(array)
