#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

from audioCmd import *

class cAudioServer(cAudioCmd):
	SUCCESS_RESULT={'success':True, 'message':None, 'data':None}
	UNKNOWN_RESULT={'success':False, 'message':'Unknown', 'data':None}
	FORMAT_ERR_RESULT={'success':False, 'message':'Command Format Error', 'data':None}
	CARD_MISSING_ERR_RESULT={'success':False, 'message':'Card is missing', 'data':None}

	# Convert a line (json array) to list for processing
	# return a dict with keys
	#	'success': true/false
	#	'message':<string>
	#	'data':json object (python <dict>)
	# In : json array in string 
	# Ret : list type object - json array
	#       none - fail (basecalss behavior)
	def _process(self, line):
		#convert json string to python list 
		obj=json.loads(line)
		if not type(obj) is list:
			return None
		return obj


	# In : routine - to process the input json array string and
	#	             return the result in another json object
	#
	def __init__(self):
		super(cAudioServer, self).__init__()


	#supposed to be called by server
	def server(self):
		while True:
			try:
				ppIn=open(self.WPIPE_NAME, 'r')
				line=ppIn.readline()[:-1]
				ppIn.close()
				ret=self._process(line)
				if not type(ret) is dict:
					ret=self.UNKNOWN_RESULT
				ppOut=open(self.RPIPE_NAME, 'wt')
				ppOut.writelines('%s\n' %json.dumps(ret))
				ppOut.close()
			except:
				print '\nProgram exits'
				break

