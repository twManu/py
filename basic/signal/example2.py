import signal
import time

class GracefulInterruptHandler(object):
	def __init__(self, sig=signal.SIGINT):
		self.sig = sig
	def __enter__(self):
		self._interrupted = False
		self.released = False
		self.original_handler = signal.getsignal(self.sig)
	
		def handler(signum, frame):
			self.release()
			self._interrupted = True
		signal.signal(self.sig, handler)
		return self

	def __exit__(self, type, value, tb):
		self.release()

	def release(self):
		if self.released: return False
		signal.signal(self.sig, self.original_handler)
		self.released = True
		return True

with GracefulInterruptHandler() as h:
	for i in xrange(1000):
		print "..."
		time.sleep(1)
		if h._interrupted:
			print "interrupted!"
			time.sleep(2)
			break