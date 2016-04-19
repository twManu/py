#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

import os, sys, re, subprocess, glob


#DEVICE=('audio', 'mixer', 'dsp', 'adsp', 'controlC', 'pcmC')
DEVICE=('controlC', 'pcmC')
DOMAIN=('QTS', 'container')

def log(string):
	if not string: return
	cmd='echo '+string+' >>/tmp/log'
	os.system(cmd)

# Gievn kernel name of device, return dev number, say controlC2=>2
# In : devNode - device node
# Ret: device number
def findDevNum(devNode):
	for prefix in DEVICE:
		myRe=re.escape(prefix)+r'(\d+)'
		match=re.search(myRe, devNode, re.I)
		if match: return match.group(1)
	return None

class cAudio(object):
	# Collect those nodes needs to be duplicated
	def _getTriggerNode(self, dirPath):
		for ff in glob.glob(dirPath+'/*'):
			for prefix in DEVICE:
				if prefix in ff:
					self._triggerPath.append(ff)

	def __init__(self, devPath, number):
		self._devPath=None
		#record, name, path and pnp path
		self._devPath=devPath
		self._devNum=str(number)
		self._triggerPath=[]
		level=0
		log('manutest 1')
		while True:
			dirName=os.path.dirname(devPath)
			devPath=os.path.basename(devPath)
			log('manutest '+dirName)
			if level == 0:
				self._devNode=devPath
				self._getTriggerNode(dirName)
			level+=1
			#find id
			if os.path.exists(dirName+'/id'):
				cmd='cat '+dirName+'/id'
				p=subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
				self._devName=p.stdout.read().strip()
			#find pnp node
			if os.path.exists(dirName+'/remove'):
				self._pnpNode=dirName
				break
			if dirName == '/': break
			devPath=dirName
		'''
		print self._devName+'(card: '+str(self._devNum)+' '+self._devNode+')'\
			+' is controlled by '+self._pnpNode
		if len(self._triggerPath):
			print 'trigger: '
			for pp in self._triggerPath:
				print '\t'+pp
		'''

	def addDb(self, fpath):
		with open(fpath, 'a+') as wfd:
			wfd.writelines("[%s] %s %s\n" %(self._devNum, self._devName, self._pnpNode))
			for pp in self._triggerPath:
				wfd.writelines("%s\n" %pp)
				#cmd='udevadm test '+pp
				#os.system(cmd)


g_db='/tmp/.au.db'
g_found=False
devNum=findDevNum(sys.argv[1])
pattern='['+str(devNum)+']'
if os.path.isfile(g_db):
	with open(g_db, 'r') as rfd:
		for line in rfd:
			if pattern in line:
				g_found=True
				break
	rfd.close()
else:
	#empty create
	os.system(' >'+g_db)

if not g_found:
	log('not found upon '+sys.argv[1]+' '+devNum)
	aud=cAudio(sys.argv[1], devNum)
	log('aud create')
	aud.addDb(g_db)

