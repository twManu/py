import os

"""
decorator of class method to concatenate gpiochip#GROUP and gpio#PIN
In :
	path - common path full name of "gpiochip" and "gpio"
	func - soc specific function to turn group/pin into suffix of "gpiochip" and "gpio"
	       the func only returns two number or string 
"""
def path_chip_map(path):
	def deco_map(func):
		def func_wrapper(*args, **kwargs):
			p1, p2 = func(*args, **kwargs)
			if p1 is None:
				if p2 is None:
					return None, None
				else:
					return None, path+'/gpio'+str(p2)
			return path+'/gpiochip'+str(p1),\
			       path+'/gpio'+str(p2)
		return func_wrapper
	return deco_map


#
# Usage
#      //input as default
#      obj=gpio(group, pin)
#      if obj:
#          obj.out(1)
#
class gpio(object):
	GPIO_PATH='/sys/class/gpio'
	STA_UNEXPT=1
	STA_EXPT=2
	DIR_IN=1
	DIR_OUT=0
	"""make sure pin exported """
	def __init__(self, chip, group, pin):
		self._status = self.STA_UNEXPT
		self._dir = self.DIR_IN
		self._chip = chip
		"""xxx_getPin existence """
		methodName = self._chip+'_getPin'
		if not methodName in gpio.__dict__:
			print self._chip+' does not support'
			return
		func = getattr(self, methodName)
		self._group, self._pin = func(group, pin)
		#print self._group, self._pin
		"""check if already exported """
		if os.path.exists(self._pin):
			self._status = self.STA_EXPT
		else:
			print "todo export"

	
	def doExport(self):
		#todo
		cmd = 'echo '+str(self._pin)+' >'+GPIO_PATH+'/export'
		sys(cmd)
		if not file.exist(self._path):
			return NIL
		self._status = STA_EXPT
		self._dir = DIR_IN
		return self._path
		
	def doUnexport(self):
		if STA_UNEXPT == self._status:
			return self._path
		cmd = 'echo '+str(self._pin)+' >'+GPIO_PATH+'/unexport'
		sys(cmd)
		self._status = STA_UNEXPT
		self._dir = DIR_IN
	
	@path_chip_map(GPIO_PATH)
	def am57_getPin(self, chip, pin):
        	"""chip=1-8, pin=0-31 """
	        if chip<=0 or chip>8:
        	        return None, None
        	chip = chip - 1
        	if pin<0 or pin>=32:
                	return None, None
	        return chip, 32*chip+pin

	# In  : in - 0 means output
	#    otherwise means input
	# Ret : NIL - direction not applied
	#       command applied
	def direction(self, input):
		cmd = ''
		if DIR_IN == self._dir:
			if not input:
				cmd = 'echo in'	
		else:        #output now
			if not input:
				cmd = 'echo out'
		if cmd:
			cmd += ' >'+self._path+'/direction'
			sys(cmd)
		return cmd
	
	# Ret : NIL not an input pin
	#      0 or 1
	def get(self):
		if STA_EXPT == self._status:
			if DIR_IN == self._dir:
				print 'echo the result'
				return 0 or 1
		return NIL
		
	# In  : value - 0 or not 0
	# Ret : NIL - fail to set value
	#       1 - value applied
	def set(self, value):
		if not STA_EXPT == self._status:
			return NIL
		if not DIR_OUT == self._dir:
			return NIL
			#echo 1 or 0
		return 1

#
# main
#
if __name__ == '__main__':
	obj=gpio('am57', 3, 26)
