import sqlite3 as db
from sip import *
import time,datetime

class sqldb:
	dbname = "/home/pi/192.168.1.64/share/ys/inverter/test.db"
	def __init__(self):
		pass
	def checkip(self,IP):
		cmd = "select * from SILowPowerInfo where IP = '%s'" % IP
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row
		return "error" 

	def getAllSinum(self):
		cmd = "select SINum from SILowPowerInfo " 
		conn = db.connect(self.dbname)
		c = conn.cursor()
		c.execute(cmd)
		rows = c.fetchall()
		conn.close()		
		return rows

	def deletetemp(self):
		cmd = "delete from SILowParameters_Temp"
		conn = db.connect(self.dbname)
		c = conn.cursor()
		c.execute(cmd)
		conn.commit()
		conn.close()

	def SaveTempParameters(self,sip):
		sip.DayPower = 0.00
		sip.SaveDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		sip.SaveDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		sip.RecDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		cmd = "insert into SILowParameters_Temp (SINum,AC_V,AC_A,AC_P,A_A,A_V,B_A,B_V,C_A,C_V,DC1_V,DC1_A, \
				DC1_P,DC2_V,DC2_A,DC2_P,T,Hz,DayPower,AllPower,Exception,SaveDate,RecDate) \
				values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
				%s,%s,%s,'%s','%s','%s')" % \
				(sip.SINum,sip.AC_V,sip.AC_A,sip.AC_P,sip.A_A,sip.A_V,sip.B_A,sip.B_V, \
				sip.C_A,sip.C_V,sip.DC1_V,sip.DC1_A, \
				sip.DC1_P,sip.DC2_V,sip.DC2_A,sip.DC2_P,sip.T,sip.Hz, \
				sip.DayPower,sip.AllPower,sip.Exception,sip.SaveDate,sip.RecDate)
		#print cmd
		conn = db.connect(self.dbname)
		c = conn.cursor()
		c.execute(cmd)
		conn.commit()
		conn.close()
		return

	def GetTopParameters(self,sinum):
		cmd = "select *  from SILowParameters_Temp  where \
			julianday('now','localtime')*86400 - julianday(RecDate)*86400 \
			<720 and SINum={num} order by id desc limit 0,1".format(num=sinum)
		#print cmd
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row
		return None

	def SaveParameters(self,sinum):
		row = self.GetTopParameters(sinum)
		if not row is None:
			savedate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			recdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			hour = recdate[-8:-6]
			minute = recdate[-5:-3]
			#print hour,minute
			#print row
			si =sip()
			si.SINum = sinum
			#print row
			si.AC_V = row[3]
			si.AC_A = row[4]
			si.AC_P = row[5]
			si.A_v = row[6]
			si.A_A = row[7]
			si.B_A = row[8]
			si.B_V = row[9]
			si.C_A = row[10]
			si.C_V = row[11]
			si.Hz = row[12]
			si.DC1_V = row[13]
			si.DC1_A = row[14]
			si.DC1_P = row[15]
			si.DC2_V = row[16]
			si.DC2_A = row[17]
			si.DC2_P = row[18]
			si.T = row[19]
			si.DayPower = row[20]
			si.AllPower = row[21]
			si.SaveDate = savedate
			si.RecDate = savedate
			si.RecGroup = int(hour)*5+(int(minute)/12)
			cmd = "insert into SILowParameters(SINum,AC_V,AC_A,AC_P,A_A,A_V,B_A,B_V,C_A,C_V,DC1_V,DC1_A, \
				DC1_P,DC2_V,DC2_A,DC2_P,T,Hz,DayPower,AllPower,Exception,SaveDate,RecDate,RecGroup) \
				values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
				%s,%s,%s,'%s','%s','%s','%s')" % \
				(si.SINum,si.AC_V,si.AC_A,si.AC_P,si.A_A,si.A_V,si.B_A,si.B_V, \
				si.C_A,si.C_V,si.DC1_V,si.DC1_A, \
				si.DC1_P,si.DC2_V,si.DC2_A,si.DC2_P,si.T,si.Hz, \
				si.DayPower,si.AllPower,si.Exception,si.SaveDate,si.RecDate,si.RecGroup)
			#print cmd
			conn = db.connect(self.dbname)
			c = conn.cursor()
			c.execute(cmd)
			conn.commit()
			conn.close()
		return

	def GetLowInverterList(self):
		cmd = "select * from (select d.*,ifnull(s.AC_P,0) as AC_P,ifnull(s.AC_V,0) as AC_V,ifnull(s.AC_A,0) \
				as AC_A,ifnull (s.Hz,0) as Hz, ifnull(s.DayPower,0) as DayPower,ifnull(s.AllPower,0) as AllPower, \
				ifnull(s.Exception,' ') as Exception from(select b.*,a.RecDate as RecDate  from(select * from silowpowerinfo)b \
				left join (select case when julianday('now','localtime')*86400 - julianday(max(RecDate))*86400 <60 \
				then max(RecDate) else null end as RecDate,siNum from SILowParameters_Temp group by siNum) a on \
				a.sinum=b.sinum) d left join SILowParameters_Temp s on  \
				s.sinum = d.sinum and d.RecDate= s.RecDate)tmp"
		conn = db.connect(self.dbname)
		c = conn.cursor()
		c.execute(cmd)
		rows = c.fetchall()
		conn.close()
		return rows

	def GetSumACP(self):
		cmd ="select ifnull(sum(AC_P),0) as AC_P,ifnull(sum(DayPower),0) as DayPower ,\
			ifnull(sum(AllPower),0) as AllPower from (select AC_P,DayPower, AllPower ,max(RecDate)\
			from silowparameters_temp where julianday('now','localtime')*86400 - julianday(RecDate)*86400 <60  \
			group by sinum)"
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row
		return 0

	def  GetSumDaypower(self):
		cmd ="select ifnull(sum(DayPower),0) as DayPower ,ifnull(sum(AllPower),0) as AllPower from \
			( select DayPower,AllPower from silowparameters where date('localtime','now')=\
			strftime('%Y%m%d',SaveDate) group by sinum)"
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row
		return 0

	def  GetSumAllpower(self):
		cmd ="select ifnull(sum(AllPower),0) as AllPower from \
		( select max(AllPower) as AllPower from silowparameters group by sinum)"
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row[0]
		return 0

	def GetACPBySinum(self,sinum):
		cmd ="select ifnull(AC_P,0),ifnull(DayPower,0), ifnull(AllPower,0) \
		from silowparameters_temp where julianday('now','localtime')*86400 - julianday(RecDate)*86400 <60 and \
		sinum = %s" % sinum
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row
		return [0,0,0]

	def  GetDaypowerBySinum(self,sinum):
		cmd ="select ifnull(DayPower,0),ifnull(AllPower,0) ,ifnull(SaveDate,'2001-01-01') \
			from silowparameters where date('localtime','now')=\
			strftime('%Y%m%d',SaveDate) and sinum = {num}  order by SaveDate desc limit 0,1".format(num=sinum) ;
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row
		return [0,0,'2001-01-01']

	def  GetAllpowerBySinum(self,sinum):
		cmd ="select ifnull(max(AllPower),0) as AllPower from silowparameters where sinum = {num} ".format(num=sinum);
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row[0]
		return [0]

	def GetParametersBySINum(self,sinum):
		cmd = "select * from SILowParameters_Temp where SINum= {num} and  \
			(julianday('now','localtime')*86400 - julianday(RecDate)*86400)<60  order by RecDate desc limit 0,1".format(num=sinum)
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return row
		return None		

	def CheckSinum(self,sinum):
		cmd ="select * from silowpowerinfo where SINum ={num}".format(num=sinum)
		conn = db.connect(self.dbname)
		c = conn.cursor()
		for row in c.execute(cmd):
			conn.close()
			return 1
		return 0

	def  GetDayACPLine(self,sinum,day):
		cmd ="select RecGroup,AC_P,time(RecDate) as RecDate from SILowParameters where \
			strftime('%Y%m%d','{recdate}')=strftime('%Y%m%d',RecDate) and SINum={num}".format(recdate = day,num = sinum)
		conn = db.connect(self.dbname)
		c = conn.cursor()
		c.execute(cmd)
		rows = c.fetchall()
		conn.close()		
		return rows

	def GetDayPowerLine(self,sinum,day):
		if sinum != '0' :
			cmd =  "select (RecGroup/5) as RecGroup,DayPower as hourpower,DayPower,time(RecDate/5) as hour from SILowParameters \
				where strftime('%Y%m%d','{recdate}')=strftime('%Y%m%d',RecDate) and \
				SINum={num}  group by (RecGroup/5)".format(recdate = day,num = sinum)
		else :
			cmd="select (RecGroup/5) as RecGroup,sum(DayPower) as hourpower,sum(DayPower)as DayPower,time(RecGroup/5) as hour \
				from (select sinum ,RecGroup as RecGroup,DayPower as hourpower, \
				DayPower,time(RecDate) as hour from SILowParameters where strftime('%Y%m%d','{recdate}')= \
				strftime('%Y%m%d',RecDate) group by sinum,RecGroup/5) group by \
				RecGroup/5".format(recdate = day)
		#print cmd
		conn = db.connect(self.dbname)
		c = conn.cursor()
		c.execute(cmd)
		rows = c.fetchall()
		conn.close()		
		return rows

	def GetMonthPowerLine(self,sinum,day):
		if sinum != '0' :
			cmd =  "select ifnull(max(DayPower),0) as DayPower  from SILowParameters \
					where strftime('%Y%m%d','{recdate}')=strftime('%Y%m%d',RecDate) \
					and  SINum={num}".format(recdate = day,num = sinum)
		else :
			cmd="select ifnull(sum(DayPower),0) as DayPower from(select max(DayPower) as DayPower \
                from SILowParameters where strftime('%Y%m%d','{recdate}')=strftime('%Y%m%d',RecDate) \
                group by sinum)".format(recdate = day)
		#print cmd
		conn = db.connect(self.dbname)
		c = conn.cursor()
		c.execute(cmd)
		rows = c.fetchall()
		conn.close()		
		return rows

	def GetYearPowerLine(self,sinum,day):
		if sinum != '0' :
			cmd =  "select ifnull(max(DayPower),0) as DayPower  from SILowParameters \
					where strftime('%Y%m','{recdate}')=strftime('%Y%m',RecDate) \
					and  SINum={num}".format(recdate = day,num = sinum)
		else :
			cmd="select ifnull(sum(DayPower),0) as DayPower from(select max(DayPower) as DayPower \
                from SILowParameters where strftime('%Y%m','{recdate}')=strftime('%Y%m',RecDate) \
                group by sinum)".format(recdate = day)
		#print cmd
		conn = db.connect(self.dbname)
		c = conn.cursor()
		c.execute(cmd)
		rows = c.fetchall()
		conn.close()		
		return rows