import subprocess, os, sys, re, glob

#busy ps has no options

class cPS(object):
	# Given a process, get its id string and process name. And also that of its parent 
	# In : idOrName - a string represent the id or process name of a process
	# 
	def __init__(self, idOrName):
		self._id=None
		self._name=None
		self._ppid=None
		#determine id
		if re.match(r'^\d+$', idOrName):         #id string provided
			self._id=str(idOrName)
		else:                                    #process name provided
			self._name=idOrName
			cmd='ps aux| grep '+self._name
			lines=[]
			p=subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
			#guess among the match commands 
			for line in iter(p.stdout.readline, b''):
				line=line.strip()                #remove empty line
				if line and not self._id:
					myRe=r'\d+:\d+\ +'+re.escape(self._name)+r'$'
					if re.search(myRe, line):
						self._id=line.split()[1]
						break
		#determine pid, and name if none
		if self._id:
			path='/proc/'+self._id+'/stat'
			if os.path.exists(path):
				p=subprocess.Popen(['cat '+path], stdout=subprocess.PIPE, shell=True)
				words=p.stdout.read().split()
				if not self._name:
					# remove '(' and then ')'
					self._name=words[1].strip('(').strip(')')
				self._ppid=str(words[3].strip())

	# Return the pid string and process name. Any of them can be None
	def getPid(self):
		return self._id

	def getProcName(self):
		return self._name

	# Return the parent pid string
	def getPpid(self):
		return self._ppid


obj=cPS(sys.argv[1])
print obj.getPid()+' ('+obj.getProcName()+') ... parent '+obj.getPpid()
