#!/usr/bin/python
#

import os, sys, re, argparse, glob

class path(object):
	TYPE_NONE=0                    #invalid
	TYPE_LINK=1
	TYPE_FILE=2
	TYPE_DIR=3

	# In  : path - if not provided, use current directory
	# Out : _parentDir, _pathName, _type
	def __init__(self, path=""):
		self._pathName=""                #the key, full path
		self._parentName=""              #full path
		self._type=self.TYPE_NONE
		#normalize
		if path:
			if re.match(r"~", path):
				path=os.path.expanduser(path)
			if os.path.exists(path):
				self._pathName=os.path.abspath(path)
		else:
			self._pathName=os.getcwd()
		self._type = self.getType(self._pathName)
		if self._type != self.TYPE_NONE:
			#leave parent "" if this is root dir
			if self._pathName != "/":
				self._parentName=os.path.dirname(self._pathName)
		#print self._pathName, self._type, self._parentDir

	# Given path, return its type and display name
	# if not provided, return path type of this object
	def getType(self, path=""):
		if path:
			if os.path.islink(path): return self.TYPE_LINK
			elif os.path.isdir(path): return self.TYPE_DIR
			elif os.path.isfile(path): return self.TYPE_FILE
			else: return self.TYPE_NONE
		return self._type

	# Given type, return display name
	def getTypeName(self, theType):
		intType=int(theType)
		if intType == self.TYPE_FILE:
			return "file"
		elif intType == self.TYPE_LINK:
			return "link"
		elif intType == self.TYPE_DIR:
			return "dir"
		else:
			return "none"


	# Return path name
	def getPath(self):
		return self._pathName

	# Return parent dir name
	def getParent(self):
		return self._parentName


#
# main
#
if __name__ == '__main__':
	testPath=("", "/", ".", "..", "/etc/vtrgb", "~/.bashrc")

	for pp in testPath:
		thisDir=path(pp)
		print "Path="+thisDir.getPath()+", type="+thisDir.getTypeName(thisDir.getType()),
		print "Parent="+thisDir.getParent()
