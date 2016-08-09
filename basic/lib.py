#!/usr/bin/python
#
# probably you need to do
# 	sys.path.append(../basic)
import subprocess, os, sys, re, argparse

class manuLib(object):
	OS_WINDOWS="WINDOWS"
	OS_MAC="MAC"
	OS_LINUX="LINUX"
	OS_UNKNOWN="UNKNOWN"
	#
	# Determine system things
	# Out: self._os
	#
	def __init__(self, debug=False):
		self._os=sys.platform
		self._isRoot=False
		self._debug=debug
		if self._os == 'win32':
			self._os=self.OS_WINDOWS
		elif self._os == 'darwin':
			self._os=self.OS_MAC
		elif 'linux' in self._os:
			self._os=self.OS_LINUX
		else:
			self._os=self.OS_UNKNOWN
		#update _isRoot if necessary
		self._checkRoot()

	# msg - message to print
	# newLine - False means 'print xxx,'
	def _DBG(self, msg, newLine=True):
		if not self._debug: return
		if newLine: print msg
		else: print msg,


	#
	# Ret: OS_XXX
	#
	def getOS(self):
		return self._os

	
	#
	# Execute command with shell and get iterator of output line
	#     usage:
	#		for line in lib.cmdOutput('ls -l'):
	#			line = line.strip()
	#			if line:
	#				print line
	# In  : cmd - command string for shell execution
	# Ret : iterator of output line
	#
	def cmdOutput(self, cmd):
		p=subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
		return iter(p.stdout.readline, '')


	# Check if user has root privilege under Mac or Linux
	# In  : self._os
	# Out : self._isRoot
	#
	def _checkRoot(self):
		if self._os==self.OS_MAC or self._os==self.OS_LINUX:
			for line in self.cmdOutput('id'):
				if re.search('(root)', line):
					self._isRoot=True


	# check if a root
	# Ret : True - user has root privileged
	#       False - otherwise
	def isRoot(self):
		return self._isRoot
#end manuLib

#
# main
#
if __name__ == '__main__':
	mylib = manuLib()
	print mylib.getOS()
	for line in mylib.cmdOutput('ls -l'):
		words=line.split()
		#print len(words)
		if len(words)>=3:          #ignore statistics
			print line.strip()

