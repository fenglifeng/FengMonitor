from config.url import urls
import multiprocessing
import web
web.config.debug = False
def tcpthread():
	from inverter.tcpserver import tcpserver
	pass

app = web.application(urls,globals())

if __name__ == '__main__':
	p = multiprocessing.Process(target=tcpthread)
	p.start()
	app.run()
