class gpioMap(object):
	def __init__(self, chip):
		self._map = NIL
		if chip = "AM5728":
			self._map = _am57Map

	# Linear, valid 0-287
	def _am57Map(self, pin):
		if pin >= 288:
			return NIL
		return pin

GPIO_PATH=/sys/class/gpio

class gpio(object):
	def __init__(self, chip):
		self._map = gpioMap(chip)
		if not self._map:
			print chip+" not support"
	
	def doExport(self, pin):
		cmd = 'echo '+self._map(pin)+' >'+GPIO_PATH+'/export'
		sys(cmd)
		if exist GPIO_PATH+'/gpio'+str(pin)
		
