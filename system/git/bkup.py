#!/usr/bin/python

import re, commands, sys, os, argparse

class git(object):
	#fail and exit with message
	def _exit(self, msg):
		print msg
		sys.exit(-1)


	#init with url or working directory
	# In  :
	#	url - first priority check with url
	#	wdir - working directory, default as current directory
	#
	def __init__(self, url='', wdir='.', verbose=0):
		self._verbose = verbose
		self._cmdPrefix = ''           #for git command 'cd path; git' XXXX
		self._remoteDB = {}
		if url:
			self._url=url
			if re.search(r':', url):
				# user provide a remote repository
				self._local = self.clone()
			elif os.path.isdir(url):
				# user provide a file path repository
				self._local = self.clone(wdir)
				self.getRemote()
			else:
				self._exit('missing url')
		elif wdir:
			# user provide a local working directory
			self._local = self._absPath(wdir)
			if self._local:
				path = self._local+'/.git'
				if not os.path.isdir(path):
					self._exit(self._local+' is not a git directory')
				self.getRemote()
				if not self._remoteDB:
					self._exit('missing remote url')
				elif 'origin(push)' in self._remoteDB:
					self._url = self._remoteDB['origin(push)']
				elif 'origin(fetch)' in self._remoteDB:
					self._url = self._remoteDB['origin(fetch)']
				else:
					self._exit('missing origin')
			else:
				self._exit('missing working directory')
		else:
			self._exit('missing parameter')
		self._cmdPrefix = 'cd '+self._local+'; git '
		self._fname = self._gitName(self._local)
		if self._verbose:
			print 'git url:', self._url
			print 'git dir:', self._local


	# return remote info
	# In  :
	#	_local - must be the local directory
	#	force - re-get remote database
	# Out : full dict if remote database
	def getRemote(self, force=False):
		if self._verbose:
			print 'Querying remote of', self._local
		if not force and self._remoteDB:
			return self._remoteDB
		self._remoteDB = {}          #clear
		cmd = 'cd '+self._local+'; git remote -v'
		for line in commands.getoutput(cmd).split('\n'):
			line = line.strip()
			if line:
				words = line.split()
				self._remoteDB[words[0]+words[2]] = words[1]
		return self._remoteDB


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
	#	_url - url to clone
	#	cdPath - directory to clone
	#	     default is curent directory
	#	name - new name
	#	     default is repository name
	# Ret: path cloned, including repository name
	def clone(self, cdPath='.', name=''):
		if self._verbose:
			print 'Cloning', self._url,
		#todo existence
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
		os.system(cmd)
		if not os.path.isdir(path+'/.git'):
			self._exit('missing '+path+'/.git')
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
		rp = git(wdir=arg.path, verbose=arg.verbose)
		if arg.query:
			print rp.getRemote()
			rp.status()
		#rp.backup()
	elif arg.url:
		rp = git(url=arg.url, verbose=arg.verbose)
	else:
		print 'no url provided'

