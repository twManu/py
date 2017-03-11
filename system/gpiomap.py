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


class gpio(object):
	GPIO_PATH=/sys/class/gpio
	STA_UNEXP=1
	STA_EXP=2
	DIR_IN=1
	DIR_OUT=0
	def __init__(self, pin):
		self._pin = pin
		self._status = UNEXP
		self._dir = DIR_IN
		self._path = GPIO_PATH+str(pin)
	
	def doExport(self):
		if STA_EXP = self._status:
			return self._path
		cmd = 'echo '+str(self._pin)+' >'+GPIO_PATH+'/export'
		sys(cmd)
		if not file.exist(self._path):
			return NIL
		self._status = STA_EXP
		self._dir = DIR_IN
		return self._path
		
	def doUnexport(self):
		if STA_UNEXP = self._status:
			return self._path
		cmd = 'echo '+str(self._pin)+' >'+GPIO_PATH+'/unexport'
		sys(cmd)
		self._status = STA_UNEXP
		self._dir = DIR_IN
	
	# In  : in - 0 means output
	#    otherwise means input
	# Ret : NIL - direction not applied
	#       command applied
	def direction(self, in):
		cmd = ''
		if DIR_IN = self._dir:
			if not in:
				cmd = 'echo in'	
		else:        #output now
			if not in:
				cmd = 'echo out'
		if cmd:
			cmd += ' >'+self._path+'/direction'
			sys(cmd)
		return cmd
	
	# Ret : NIL not an input pin
	#      0 or 1
	def get(self):
		if STA_EXP = self._status:
			if DIR_IN = self._dir:
				echo the result
				return 0 or 1
		return NIL
		
	# In  : value - 0 or not 0
	# Ret : NIL - fail to set value
	#       1 - value applied
	def set(self, value):
		if not STA_EXP = self._status:
			return NIL
		if not DIR_OUT = self._dir:
			return NIL
			#echo 1 or 0
		return 1