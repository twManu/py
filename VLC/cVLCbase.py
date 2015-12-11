from distutils import spawn
import time

class cVLCbase(object):
	NONE = 0
	FILE = 10                                #reserve 9 sub-type for each
	ATV = 20
	DTV = 30

	# [_command, _arg] will be used to run VLC
	def __init__(self, type = NONE):
		self._type = type                #to show user   
		self._command = 'vlc'
		self._arg = ""
		self._Tstart = 0

	def config(self, param):
		self._arg += param

	def _diffStart(self):
		t2 = time.clock()       #sec
		t2 -= self._Tstart
		str = ""
		if t2 > 24*60*60:
			tmp = t2 / (24*60*60)
			str.append('{0:02d}'.format(tmp) + "d ")
			t2 %= 24*60*60
		if t2 > 60*60:
			tmp = t2 / (60*60)
			str.append('{0:02d}'.format(tmp) + ":")
			t2 %= 60*60
		else:
			str.append("00:")
		if t2 > 60:
			tmp = t2 / 60
			str.append('{0:02d}'.format(tmp) + ":")
			t2 %= 60
		else:
			str.append("00:")
		str.append('{0:02d}'.format(t2))
		return str

	def start(self):
		if None == spawn.find_executable(self._command):
			print(self._command + " doesn't exist")
		else:
			self._Tstart = time.clock()
			#catch stderr
			self._proc = subprocess.Popen(self.getCmd(),
					stderr=subprocess.PIPE)
			self.process()

	#return json object of command, should be ['vlc', <arg>]
	def getCmd(self):
		return [self._command, self._arg]

	#return readable string of type of command
	#sub class can define its string say ATSC
	def getType(self):
		if self.NONE == self._type:
			return "NONE"
		elif self.FILE == self._type:
			return "FILE"
		elif self.ATV == self._type:
			return "ATV"
		elif self.DTV == self._type:
			return "DTV"
		return "Unknown"

	#to be overwritten
	#used to 
	def process(self):
		for line in iter(self._proc.stderr.readline,''):
			print "[" + self._diffStart() + "] " + line.rstrip()

if __name__ == '__main__':
	obj = cVLCbase()
	print(obj.getType())
	print(obj.getCmd())
	obj.start()
