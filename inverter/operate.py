from sqldb import *
import calendar

def GetMainInfo():
	mysql = sqldb()
	row = mysql.GetSumACP()
	ac_p = row[0]
	daypower = row[1]
	allpower = row[2]
	if daypower == 0 :
		row = mysql.GetSumDaypower()
		daypower = row[0]
		allpower = row[1]
		if allpower == 0 :
			allpower = mysql.GetSumAllpower()
	return (ac_p,daypower,allpower)

def GetReMainInfo():
	mysql = sqldb()
	row = mysql.GetSumACP()
	ac_p = row[0]
	daypower = row[1]
	allpower = row[2]
	if daypower == 0 :
		row = mysql.GetSumDaypower()
		daypower = row[0]
		allpower = row[1]
		if allpower == 0 :
			allpower = mysql.GetSumAllpower()
	result = [0,0,0]
	result[0] = ac_p
	result[1] = daypower
	result[2] = allpower
	return result

def GetMainInfoBySinum(sinum):
	mysql = sqldb()
	row = mysql.GetACPBySinum(sinum)
	ac_p = row[0]
	daypower = row[1]
	allpower = row[2]
	if daypower == 0 :
		row = mysql.GetDaypowerBySinum(sinum)
		daypower = row[0]
		allpower = row[1]
		if allpower == 0 :
			allpower = mysql.GetAllpowerBySinum(sinum)
	result = [0,0,0]
	result[0] = ac_p
	result[1] = daypower
	result[2] = allpower
	return result

def GetParametersBySinum(sinum):
	mysql = sqldb()
	row = mysql.GetParametersBySINum(sinum)
	return row

def CheckSinum(sinum):
	mysql = sqldb()
	return mysql.CheckSinum(sinum)

def GetDayACPLine(sinum,day):
	mysql = sqldb()
	rows = mysql.GetDayACPLine(sinum,day)
	datas = [0 for i in range(120)]
	index = 0
	for row in rows :
		while index < (row[0]-1) :
			datas[index] = 0
			index = index + 1
		datas[index] = row[1]
		index = index + 1
	while index<120:
		datas[index] = 0
		index = index + 1
	return datas

def GetDayPowerLine(sinum,day):
	mysql = sqldb()
	rows = mysql.GetDayPowerLine(sinum,day)
	datas = [0 for i in range(24)]
	index = 0
	prepower = 0
	for row in rows :
		while index < (row[0]-1) :
			datas[index] = 0
			index = index + 1
		datas[index] = row[1] - prepower
		if row[1]>prepower :
			prepower = row[1]
		else :
			datas[index] = 0
		index = index + 1
	while index<24:
		datas[index] = 0
		index = index + 1
	return datas

def GetMonthPowerLine(sinum,year,month):
	mysql = sqldb()
	days =  calendar.monthrange(int(year),int(month))[1]
	datas = [0 for i in range(days)]
	index = 0
	prepower = 0
	for i in range(1,days+1):
		day = i
		if i<10:
			day='0'+str(i)
		time = str(year)+'-'+str(month)+'-'+str(day)
		rows = mysql.GetMonthPowerLine(sinum,time)
		if len(rows) <= 0:
			datas[i-1] = '0'
		else:
			for row in rows :
				datas[i-1] = row[0]
	return datas

def GetMonthPowerLine(sinum,year):
	mysql = sqldb()
	datas = [0 for i in range(12)]
	index = 0
	prepower = 0
	for i in range(1,12):
		day = i
		if i<10:
			day='0'+str(i)
		time = str(year)+'-'+str(month)+'-'+str(day)
		rows = mysql.GetMonthPowerLine(sinum,time)
		if len(rows) <= 0:
			datas[i-1] = '0'
		else:
			for row in rows :
				datas[i-1] = row[0]
	return datas
