#!/usr/bin/python

import re, commands, sys, os, argparse

class git(object):
	def __init__(self, url, verbose=0):
		self._local = self._absPath(url)
		self._verbose = verbose
		self._cmdPrefix = ''
		if self._local:
			# user provide a local dict
			path = self._local+'/.git'
			if not os.path.isdir(path):
				print self._local, 'is not a git directory'
				sys.exit(-1)
			self._url = self.getRemote(False)
			if not self._url:
				print 'missing remote url'
				sys.exit(-1)
		else:
			# user provide a remote repository
			self._url=url
			if not self._url:
				print 'missing url'
				sys.exit(-1)
			self._local = self.clone()
		self._cmdPrefix = 'cd '+self._local+'; git '
		self._fname = self._gitName(self._local)
		print 'git url:', self._url
		print 'git dir:', self._local


	# return remote info
	# In  :
	#	_local - must be the local directory
	#	allRemote - true to return all remote in dict
	#	           false to return 1st origin
	# Out :
	#	full dict if allRemote
	#	dict['origin(push'] if not allRemote
	#	None if nothing
	def getRemote(self, allRemote=True):
		if self._verbose:
			print 'Querying remote of', self._local
		theDict = {}
		cmd = 'cd '+self._local+'; git remote -v'
		for line in commands.getoutput(cmd).split('\n'):
			line = line.strip()
			if line:
				words = line.split()
				theDict[words[0]+words[2]] = words[1]
		if allRemote:
			return theDict
		elif 'origin(push)' in theDict:
			return theDict['origin(push)']
		else:
			return None

	# return status in output
	def status(self):
		if not self._cmdPrefix:
			print 'repository might not init properly'
			return
		cmd = self._cmdPrefix+'status'
		os.system(cmd) 

			
	# return absolute path and no trailing /
	# nor ~
	def _absPath(self, thePath):
		if thePath:
			if re.match(r"~", thePath):
				thePath=os.path.expanduser(thePath)
			if os.path.exists(thePath):
				thePath=os.path.abspath(thePath)
				return thePath
		return ''


	# return name after, excluding, last '/'
	#
	def _gitName(self, thePath):
		name = ''
		match = re.search(r'[^/]+$', thePath)
		if match:
			name = match.group(0)
		return name	


	# clone repository to dir with new name
	# In :
	#	cdPath - directory to clone
	#	     default is curent directory
	#	name - new name
	#	     default is repository name
	# Ret: path cloned, including repository name
	def clone(self, cdPath='.', name=''):
		if self._verbose:
			print 'Cloning', self._url,
		#comopse command and path
		path = cdPath
		cmd = ''
		if cdPath:
			cmd += 'cd '+cdPath+';'
		cmd += 'git clone '+self._url
		if name:
			cmd += ' '+name
		else:
			name = self._gitName(name)
			if self._verbose:
				print 'to ... ' + name
		path += '/'+name
		path = os.path.abspath(path)
		#run clone
		commands.getoutput(cmd)
		if not os.path.isdir(path+'/.git'):
			print 'missing ', path+'/.git'
			sys.exit(-1)
		return path

	def backup(self, url2=''):
		target = '/tmp/'+self._fname
		os.system('git clone --bare --mirror '+self._url+' '+target)
		'''
		git remote set-url --push origin url2
		git fetch -p origin
		git push --mirror
		'''
		
		

###
#main
#
if __name__ == '__main__':
	# Parse argument and make sure there is action to be taken
	# Ret : arg - parsed result
	def check_param():
		parser = argparse.ArgumentParser()
		parser.add_argument('-d', action='store', dest='path', default='',
			help='path of local git')
		parser.add_argument('-q', action='store_true', dest='query', default=False,
			help='query status of local git')
		parser.add_argument('-u', action='store', dest='url', default='',
			help='url to remote git')
		parser.add_argument('-v', type=int, action='store', dest='verbose', default=0,
			choices=[0, 1, 2, 3])
		arg=parser.parse_args()
		return arg

	arg = check_param()
	if arg.path:
		rp = git(arg.path, arg.verbose)
		if arg.query:
			print rp.getRemote()
			rp.status()
		rp.backup()
	elif arg.url:
		rp = git(arg.url, arg.verbose)
	else:
		print 'no url provided'

