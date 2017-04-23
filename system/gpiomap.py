def deco_map(func):
	def func_wrapper(path, chip, pin):
		p1, p2 = func(chip, pin)
		if p1 is None:
			if p2 is None:
				return None, None
			else:
				return None, path+'/'+p2
		return path+'/gpiochip'+p1, path+'/gpio'+p2
	return func_wrapper

@deco_map
def am57_chip(chip, pin):
	"""chip=1-8, pin=0-31 """
	if chip<=0 or chip>8:
		return None, None
	chip = chip - 1
	if pin<0 or pin>=32:
		return None, None
	return chip, 32*chip+pin



class gpioMap(object):
	def __init__(self, chip):
		self._map = NIL
		if chip = "AM5728":
			self._map = _am57Map

 @abstractmethod
    def vehicle_type():
        """"Return a string representing the type of vehicle this is."""
        pass
	# Linear, valid 0-287
	def _am57Map(self, pin):
		if pin >= 288:
			return NIL
		return pin


#
# Usage
#      //input as default
#      obj=gpio(group, pin)
#      if obj:
#          obj.out(1)
#
class gpio(object):
	GPIO_PATH=/sys/class/gpio
	STA_UNEXPT=1
	STA_EXPT=2
	DIR_IN=1
	DIR_OUT=0
	def __init__(self, group, pin):
		self._status = STA_UNEXPT
		self._dir = DIR_IN
		self._group, self._pin = gpioMap(group, pin)
		
	
	def doExport(self):
		if STA_EXPT = self._status:
			return self._path
		cmd = 'echo '+str(self._pin)+' >'+GPIO_PATH+'/export'
		sys(cmd)
		if not file.exist(self._path):
			return NIL
		self._status = STA_EXPT
		self._dir = DIR_IN
		return self._path
		
	def doUnexport(self):
		if STA_UNEXPT = self._status:
			return self._path
		cmd = 'echo '+str(self._pin)+' >'+GPIO_PATH+'/unexport'
		sys(cmd)
		self._status = STA_UNEXPT
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
		if STA_EXPT = self._status:
			if DIR_IN = self._dir:
				echo the result
				return 0 or 1
		return NIL
		
	# In  : value - 0 or not 0
	# Ret : NIL - fail to set value
	#       1 - value applied
	def set(self, value):
		if not STA_EXPT = self._status:
			return NIL
		if not DIR_OUT = self._dir:
			return NIL
			#echo 1 or 0
		return 1