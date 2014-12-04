import threading
import time

class Pysettimer(threading.Thread):
	def __init__(self,function,args=None,timeout=1, \
				is_loop=False):
		threading.Thread.__init__(self)
		self.event = threading.Event()
		self.function = function
		self.args = args
		self.timeout = timeout
		self.is_loop = is_loop

	def run(self):
		while not self.event.is_set():
			self.event.wait(self.timeout)
			self.function(self.args)

			if not self.is_loop:
				self.event.set()

	def stop(self):
		self.event.set()
