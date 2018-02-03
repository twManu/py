#!/usr/bin/python

import re, commands, sys, os, argparse
sys.path.append('../path')
from libPath import *

class git(manuLib):
	#init with url or working directory
	#   for url, clone to wdir or current directory
	#   for wdir, 
	# In  :
	#	url - first priority check with url
	#	wdir - working directory, default as current directory
	#	verbose - message level
	#
	def __init__(self, url='', wdir='.', verbose=0):
		self._verbose = verbose
		self._cmdPrefix = ''           #for git command 'cd path; git' XXXX
		self._branchDB = []
		self._logDB= []
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
		self.branch()
		self._prepareCommit()


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
		path = cPath(thePath)
		return path.getPath()


	# return name after, excluding, last '/'
	# empty string returned if no name recognized
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
		path = cPath(cdPath)
		if self._verbose:
			print 'Cloning', self._url,
		#check existence
		if not name:
			name = self._gitName(self._url)
			if not name:
				self._exit('unable to get git name')
			name = name.split('.')[0]
		if self._verbose:
			print 'to ... ' + name
		target = path.cascade(name)
		if os.path.exists(target):
			ans = raw_input(target+' exists. Delete to continue (y/n)? ')
			if ans != 'y' and ans != 'Y':
				self._exit()
			print 'Deleting...', target
			os.system('rm -rf '+target)
		#comopse command and path
		cmd = ''
		if cdPath:
			cmd += 'cd '+cdPath+';'
		cmd += 'git clone '+self._url
		#run clone
		os.system(cmd)
		if not os.path.isdir(path.cascade('/.git', target)):
			self._exit('missing '+target+'/.git')
		return target


	def backup(self, url2=''):
		target = '/tmp/'+self._fname
		os.system('git clone --bare --mirror '+self._url+' '+target)
		'''
		git remote set-url --push origin url2
		git fetch -p origin
		git push --mirror
		'''

	# Do branch if init'ed
	# In  : _cmdPrefix
	#	_brandDB
	# Ret : list of branch
	def branch(self):
		if not self._branchDB:
			if self._verbose:
				print 'collect branches of', self._local
			if not self._cmdPrefix:
				return self._branchDB
			lines = commands.getoutput(self._cmdPrefix+'branch -a').splitlines()
			for line in lines:
				words = line.split()
				if re.match(r'\* ', line):
					self._branchDB.append(words[1].strip())
				else:
					self._branchDB.append(words[0].strip())
		return self._branchDB

	# Check if valid branch or commit, empty string ok
	# Ret : True - valid
	#	False - otherwise
	def _validHash(self, hashCode):
		if hashCode:
			if not hashCode in self._logDB\
				and not hashCode in self._branchDB:
					return False
		return True
		

	#print diff in stdout
	def diff(self, hashCode=''):
		if self._validHash(hasCode):
			self.exec_cmd('diff', hasCode)
		else: print 'Invalid hash', hashCode


	def addPrefix(func):
		def wrapper(self, *args, **kwargs):
			if self._cmdPrefix:
				cmd = self._cmdPrefix
				for arg in args:
					cmd += ' '+arg
				print cmd
				os.system(cmd)
		return wrapper

	# collect commit
	#In  : _cmdPrefix
	def _prepareCommit(self):
		if not self._logDB:
			lines = commands.getoutput(self._cmdPrefix+'log --oneline').splitlines()
			for line in lines:
				if not line: continue
				words = line.split()
				self._logDB.append(words[0])
			

	# query log between given two branches, or current and given branch
	# In  : br2 - oldhash
	#	br1 - newhash
	def log(self, br2, br1=''):
		if not self._validHash(br2):
			print 'Invalid hash', br2
			return None
		if not self._validHash(br1):
			print 'Invalid hash', br1
			return None
		self.exec_cmd('log ' + br2 + '..' + br1)


	#a mean to pass function user want to exec
	@addPrefix
	def exec_cmd(self, *args, **kwargs):
		pass



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
		parser.add_argument('-c', action='store', dest='cmd', default='',
			help='command, optionally arg, for git to exec')
		parser.add_argument('-l', action='store', dest='br2', default='',
			help='show log between')
		parser.add_argument('-v', type=int, action='store', dest='verbose', default=0,
			choices=[0, 1, 2, 3])
		parser.add_argument('-b', action='store_true', dest='branch', default=False,
			help='show branches')
		arg=parser.parse_args()
		return arg

	arg = check_param()
	if arg.path:
		rp = git(wdir=arg.path, verbose=arg.verbose)
	elif arg.url:
		rp = git(url=arg.url, verbose=arg.verbose)
	else:
		print 'no url provided'
		sys.exit(-1)
	# do command
	#
	if arg.query:
		db=rp.getRemote()
		if db:
			for remote in db:
				print remote+' :'+db[remote]
		rp.exec_cmd('status')
	elif arg.branch:
		print rp.branch()
	elif arg.br2:
		rp.log(arg.br2)
	elif arg.cmd:
		rp.exec_cmd(arg.cmd)
	#rp.backup()
