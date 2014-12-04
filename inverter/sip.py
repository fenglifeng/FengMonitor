import struct
import array

class sip:
	Id = 0
	SINum = 0xa5
	AC_V = 0
	AC_A = 0
	AC_P = 0
	A_A = 0
	B_A = 0
	C_A = 0
	A_V = 0
	B_V = 0
	C_V = 0
	Hz = 0
	DC1_V = 0
	DC1_A = 0
	DC1_P = 0
	DC2_V = 0
	DC2_A = 0
	DC2_P = 0
	T = 0
	IP = "0.0.0.0"
	SIStatus =" "
	Exception = " "
	DayPoer = 0
	AllPower = 0
	SaveDate = "2014-08-01"
	RecDate = "2014-08-01"

	def bytestofloat(self,buff):
		if len(buff) < 4:
			return 0
		else :
			data = [buff[1],buff[0],buff[3],buff[2]]
			buffer = struct.unpack('>f',buff)[0]
			return round(buffer,2)
	def bytestoint(self,buff) :
		if len(buff) < 4 :
			return 0
		else:
			return struct.unpack('>I',buff)[0]

	def bytestoushort(self,buff) :
		if len(buff) < 2 :
			return 0
		else:
			#return int(buff[0])<<8 + int(buff[1])
			return struct.unpack('>H',buff)[0]

	def readdata(self,buff):
		startnum = 3
		i=0
		j=i+2
		self.SINum = ord(buff[0])
		self.A_V = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 10.0
		self.AC_V = self.A_V
		i = i+2
		j = i+2 
		self.A_A = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 100.0
		self.AC_A = self.A_A
		i = i+2
		j = i+2 
		self.AC_P = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 1000.0
		i = 10  
		j = i+2 
		self.Hz = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 100.0
		i = 26
		j = i+2 
		self.DC1_V = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 10.0
		i = i+2
		j = i+2 
		self.DC1_A = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 100.0
		i = i+2
		j = i+2 
		self.DC1_P = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 1000.0
		i = i+2
		j = i+2 
		self.DC2_V = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 10.0
		i = i+2
		j = i+2 
		self.DC2_A = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 100.0
		i = i+2
		j = i+2 
		self.DC2_P = self.bytestoushort(buff[(startnum+i):(startnum+j)]) / 1000.0
		i = 42
		j = i+2 
		self.T = self.bytestoushort(buff[(startnum+i):(startnum+j)])
		i = 52
		j = i+4 
		self.DayPower = self.bytestofloat(buff[(startnum+i):(startnum+j)]) 
		i = i+4
		j = i+4 
		self.AllPower = self.bytestofloat(buff[(startnum+i):(startnum+j)])
		i = 69
		self.Exception = self.GetErrorInfo(ord(buff[startnum+i]))
		pass
		
	def GetErrorInfo(self,buff):
		return{
			1:"Grid Volt   Over  Rating ",
			2:"Grid Volt   Under Rating ",
			3:"Grid Freq   Over  Rating ",
			4:"Grid Freq   Over  Rating ",
			5:"Grid Volt   Inconsistent ",
			6:"Passive   Anti-islanding ",
			7:"OverFreq   Anti-islanding ",
			8:" UnderFreq  Anti-islanding ",
			9:"Grid Volt Phase Lose  ",
			10:"Grid Freq   Abnormal",
			11:"Output Over Current",
			12: "DCInject Excessive ",
			13:"Inverter  Abnormal ",
			14:"Relay Stick ",
			15:"UBus  Abnormal ",
			16:" Temp Abnormal ",
			17:"Relay Open ",
			18:"Residual Sensor Fail ",
			19:" Residual Over Current ",
			20:"PV Volt Under Rating",
			21:"PV Volt Over Rating ",
			22:" PV Input Ground Fault",
			}.get(buff," ")
