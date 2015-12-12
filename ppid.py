import subprocess, os, sys, re, argparse

class cPS(object):
	# get the line iterator of command output
	# Note that the line iteratored might contain empty line
	# In  : cmd - shell command to execute
	# Ret : line iterator  
	def _cmdOutLineIter(self, cmd):
		p=subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
		return iter(p.stdout.readline, b'')

	# get the ppid from /proc
	# In  : _id - process id
	# Out : _ppid - parent process id
	def _getPpid(self):
		if self._id:
			path='/proc/'+self._id+'/stat'
			if os.path.exists(path):
				p=subprocess.Popen(['cat '+path], stdout=subprocess.PIPE, shell=True)
				words=p.stdout.read().split()
				self._ppid=str(words[3].strip())

	# get the process command by pid when _name is not determined
	# In  : _id - process id
	# Out : _name - process command
	def _nameFromId(self):
		if not self._name and self._id:
			cmd='ps aux| grep '+self._id
			for line in self._cmdOutLineIter(cmd):
				line=line.strip()                #remove empty line
				if not line: continue
				words=line.split()
				if words[1] == self._id:         #pid match
					words=line.split(':')        #0:00 <command>
					name=words[len(words)-1]
					self._name=re.sub(r'\d+\ ', '', name).strip()
					break

	# get the process id from command when _id is not determined
	# In  : _name - process command
	# Out : _id - process id
	def _idFromName(self):
		if not self._id and self._name:
			cmd='ps aux| grep '+self._name
			for line in self._cmdOutLineIter(cmd):
				line=line.strip()                #remove empty line
				if not line: continue
				#0:00 <command>
				myRe=r'\d+:\d+\ +'+re.escape(self._name)+r'$'
				if re.search(myRe, line):
					self._id=line.split()[1]
					break

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
			if self._id == '0' or self._id == '1':
				self._name='init'
				self._ppid='0'
				return
			self._nameFromId()
		else:                                    #process name provided
			self._name=idOrName
			if self._name == 'init':
				self._id='1'
				self._ppid='0'
				return
			self._idFromName()
		self._getPpid()

	# Return the pid string and process name. Any of them can be None
	def getPid(self):
		return self._id

	def getProcName(self):
		return self._name

	# Return the parent pid string
	def getPpid(self):
		return self._ppid

#entry
if '__main__' == __name__:
	def usage(reason=None):
		if reason: print reason
		print '  Usage: ppid.py -p [PID | PROC_NAME] [-r LEVEL]'
		print '    show the process id and command along with parent process id'
		print '    PID - process id'
		print '    PROC_NAME - process command'
		print '    LEVEL - trace LEVEL times higher up, 0 by default'
		print '  Ret: 0 success and 1 failure'

	# process parameters
	# Ret: exit 1 if fails
	#      otherwise - parsed argument object 
	def check_param():
		parser = argparse.ArgumentParser()
		parser.add_argument('-p', action='store', dest='proc', default=None,
			help='process id or command')
		parser.add_argument('-r', action='store', dest='level', default=0,
			help='trace level higher up')

		arg = parser.parse_args()
		if not arg.proc:
			usage("Missing process parameter")
			sys.exit(1)
		return arg

	#main
	arg=check_param()
	obj=cPS(arg.proc)
	count=int(arg.level)
	while count >= 0:
		pid=obj.getPid()
		name=obj.getProcName()
		ppid=obj.getPpid()
		print pid+' ('+name+') ... parent '+ppid
		if pid == '1' or ppid == '1': break
		if name == 'init': break
		count-=1
		obj=cPS(obj.getPpid())
