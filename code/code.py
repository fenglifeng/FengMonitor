import web
from config import settings
from inverter import sqldb
from inverter import operate
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
web.config.debug = False

render = settings.render
errorinfo = "<h1>Soory,Please check your url</h1>"

class index:
	def GET(self):
		return render.index()

class top:
	def GET(self):
		return render.top()

class menu:
	def GET(self):
		return render.menu()

class weather:
	def GET(self):
		return render.weather()

class list:
	def GET(self):
		mysql = sqldb.sqldb()
		rows = mysql.GetLowInverterList()
		#print rows
		return render.list(rows)

class relist:
	def GET(self):
		mysql = sqldb.sqldb()
		rows = mysql.GetLowInverterList()
		#print rows
		return json.dumps(rows)

class test:
	def GET(self):
		pass

class main:
	def GET(self):
		ac_p,daypower,allpower = operate.GetMainInfo()
		return render.main(ac_p,daypower,allpower)

class remain:
	def GET(self):
		result = operate.GetReMainInfo()
		return json.dumps(result)

class info:
	def GET(self):
		i = web.input()
		try:
			sinum = i['sinum']
		except Exception, e:
			sinum = 0
			return errorinfo
		sinum = i['sinum']
		if operate.CheckSinum(sinum) == 0:
			return errorinfo
		rowparam = operate.GetParametersBySinum(sinum)
		rowmain = operate.GetMainInfoBySinum(sinum)
		return render.inverterinfo(sinum,rowparam,rowmain)	

class reACP:
	def GET(self):
		i = web.input()
		try:
			sinum = i['sinum']
			day = i['day']
		except Exception, e:
			sinum = 0
			return errorinfo	
		datas = operate.GetDayACPLine(sinum,day)
		return json.dumps(datas)

class reDayPower:
	def GET(self):
		i = web.input()
		try:
			sinum = i['sinum']
			day = i['day']
		except Exception, e:
			sinum = 0
			return errorinfo	
		datas = operate.GetDayPowerLine(sinum,day)
		return json.dumps(datas)

class reMonthPower:
	def GET(self):
		i = web.input()
		try:
			sinum = i['sinum']
			day = i['day']
		except Exception, e:
			sinum = 0
			return errorinfo
		array = day.split('-')
		if len(array)<2:
			return
		year = array[0]
		month = array[1]	
		datas = operate.GetMonthPowerLine(sinum,year,month)
		return json.dumps(datas)
		
class reYearPower:
	def GET(self):
		i = web.input()
		try:
			sinum = i['sinum']
			day = i['day']
		except Exception, e:
			sinum = 0
			return errorinfo
		array = day.split('-')
		if len(array)<2:
			return
		year = array[0]	
		datas = operate.GetYearPowerLine(sinum,year)
		return json.dumps(datas)

class inverterpower:
	def GET(self):
		i = web.input()
		try:
			sinum = i['sinum']
		except Exception, e:
			sinum = 0
			return errorinfo
		ac_p,daypower,allpower = operate.GetMainInfoBySinum(sinum)
		return render.inverterpower(sinum,ac_p,daypower,allpower)