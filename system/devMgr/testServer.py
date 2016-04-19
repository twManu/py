#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

from audioServer import *
from audio import *
import glob, re

class cTestServer(cAudioServer):
	# Convert a line (json array) to list for processing
	# return a response dict with keys
	#	'success': true/false
	#	'message':<string>
	#	'data':json object (python <dict>
	# Ret : dict type
	def _process(self, line):
		obj=super(cTestServer, self)._process(line)
		if not obj: return self.FORMAT_ERR_RESULT
		if obj[0] == self.CMD_INFO:
			#data is a dict
			dict={}
			for key in self._devDict.keys():
				id, domain = self._devDict[key].getInfo()
				dict[key]=[id, domain]
			response=self.SUCCESS_RESULT
			response['data']=dict
			return response
		elif obj[0] == self.CMD_ASSIGN:
			dict=obj[1]
			try:
				num=dict['card']
				if num in self._devDict.keys():
					self._devDict[num].toggle()
				else:
					return self.CARDMISSING_ERR_RESULT
			except:
				return self.UNKNOWN_RESULT
		'''
		print 'Command: '+obj[0]
		if obj[1]:
			print 'Arg: '
			for key in obj[1].keys():
				print '\t'+key+': '+str(obj[1][key])
		else:
			print 'Arg: null'
		print ''
		'''
		return self.SUCCESS_RESULT

	def __init__(self):
		self._devDict={}
		super(cTestServer, self).__init__()
		#create db
		for dd in glob.glob('/sys/class/sound/card*'):
			num=re.sub(r'.*card', '', dd)
			self._devDict[num]=cAudio(num)


obj=cTestServer()
obj.server()
