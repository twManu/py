#!/usr/bin/python
#
import subprocess, os, sys, re, argparse

class lib(object):
	OS_WINDOWS="WINDOWS"
	OS_MAC="MAC"
	OS_LINUX="LINUX"
	OS_UNKNOWN="UNKNOWN"
	#
	# Determine system things
	# Out: self._os
	#
	def __init__(self):
		self._os=sys.platform
		if self._os == 'win32':
			self._os=self.OS_WINDOWS
		elif self._os == 'darwin':
			self._os=self.OS_MAC
		elif 'linux' in self._os:
			self._os=self.OS_LINUX
		else:
			self._os=self.OS_UNKNOWN
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

#
# main
#
if __name__ == '__main__':
	mylib = lib()
	print mylib.getOS()
	for line in mylib.cmdOutput('ls -l'):
		words=line.split()
		#print len(words)
		if len(words)>=3:          #ignore statistics
			print line.strip()

