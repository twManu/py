import subprocess, os, sys, re

#busy ps has no options

class cPS(object):
	def __init__(self, idOrName):
		self._id=0
		self._name=None
		if re.match(r'^\d+$', idOrName):
			#providing id
			self._id=idOrName
			cmd='cat /proc/'+str(idOrName)+'/stat'
			p=subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
			words=p.stdout.read().split()
			# remove '('
			self._name=re.sub(r'^\(', "", words[1])
			# remove ')'
			self._name=re.sub(r'\)$', "", self._name)
			print self._name
		else:
			#providing process name
			self._name=idOrName
			cmd='ps aux |grep '+idOrName
			p=subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
			#get first line
			ln=p.stdout.read()
			self._id=ln.split()[1]
			print self._id
			

obj=cPS(sys.argv[1])