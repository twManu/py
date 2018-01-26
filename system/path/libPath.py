#!/usr/bin/python
#

import os, sys, re, argparse, glob, commands
sys.path.append('../../basic')
from lib import manuLib

class cPath(manuLib):
	TYPE_NONE=0                    #invalid
	TYPE_LINK=1
	TYPE_FILE=2
	TYPE_DIR=3

	# In  : path - if not provided, use current directory
	# Out : _parentDir, _pathName, _type
	def __init__(self, thePath, debug=False):
		super(cPath, self).__init__(debug)
		self._pathName=""                #the key, full path
		self._parentName=""              #full path
		self._type=self.TYPE_NONE
		#normalize
		if thePath:
			if re.match(r"~", thePath):
				thePath=os.path.expanduser(thePath)
			if os.path.exists(thePath):
				self._pathName=os.path.abspath(thePath)
		else:
			self._pathName=os.getcwd()
		self._type = self.getType(self._pathName)
		if self._type != self.TYPE_NONE:
			#leave parent "" if this is root dir
			if self._pathName != "/":
				self._parentName=os.path.dirname(self._pathName)
		self._DBG("Path: "+self._pathName+", Parent: "+self._parentName, False)
		self._DBG("Type: "+self.getTypeName(self._type))

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

	# Check if the path presents in subirectory
	def subExist(self, subPath, theType):
		#remove leading '/'
		subPath=re.sub(r'^/', "", subPath)
		pathObj=cPath(self._pathName+'/'+subPath)
		if pathObj.getPath() and theType == pathObj.getType():
			return True
		return False	

	# Return list of sub files
	def getSubFiles(self):
		fList=[]
		for dirPath, dirNames, fileNames in os.walk(self._pathName):
			subPath=re.sub(self._pathName, "", dirPath)
			for f in fileNames:
				fList.append(os.path.join(subPath, f))
		return fList

	# given fPath and rPath return fPath/rPath
	# In  : rearPath - rPath
	#	frontPath - fPath
	#	         if not provieded, use _pathName as frontPath
	# Ret : fPath/rPath
	def cascade(self, rearPath, frontPath=''):
                if not frontPath:
			frontPath = self._pathName
		if not rearPath: return frontPath
                #both front and rear
                frontPath = re.sub(r'/$', "", frontPath)
                rearPath = re.sub(r'^/', "", rearPath)
                return frontPath+'/'+rearPath


#
# Gievn dev node and optionally mount point
# Provide mount and umount
# Can report dev node and mount path
class partition(object):
	#node: node name under /dev
	#      can be absent since it might later be created
	#mountPath: mount point when to mount
	#      if not given, check the following
	#       1. check df
	#       2. /tmp/<node> will be used
	def __init__(self, node, mountPath=None):
		self._devNode = node
		self._devPath = '/dev/'+node
		if not os.path.exists(self._devPath):
			print "Missing "+self._devPath+" !!!"
			self._mountPath = '/run/media/'+node
			return
		if mountPath:
			self._mountPath = mountPath
		else:
			#check if mounted
			lines = commands.getoutput('df').splitlines()
			for ll in lines:
				mountDev = ll.split()[0]
				if re.match(self._devPath, mountDev, re.M|re.I):
					self._mountPath = ll.split()[5]
					return
			#not mounted
			self._mountPath = '/tmp/'+node


	def umount(self):
		#do nothing if node not present
		if not os.path.exists(self._devPath):
			return
		lines = commands.getoutput('df').splitlines()
		for ll in lines:
			mountDev = ll.split()[0]
			if re.match(self._devPath, mountDev, re.M|re.I):
				print "Umount "+mountDev
				os.system("umount "+mountDev)


	def mount(self):
		if not os.path.exists(self._devPath):
			print 'Skip mounting '+self._devPath
			return
		#make sure path exists
		os.system('mkdir -p '+self._mountPath)
		os.system('mount '+self._devPath+' '+self._mountPath)


	def devPath(self):
		return self._devPath


	def mountPath(self):
		return self._mountPath


#
# main
#
if __name__ == '__main__':
	#check path, type, and parent
	testPath=("", "/", ".", "..", "/etc/vtrgb", "~/.bashrc")
	for pp in testPath:
		thisDir=cPath(pp, os.getcwd())
		print "Path="+thisDir.getPath()+", type="+thisDir.getTypeName(thisDir.getType()),
		print ", Parent="+thisDir.getParent()
	#check subdir existence
	subDir=("init", "/init", "rc.local")
	thisDir=cPath('/etc')
	for ss in subDir:
		if thisDir.subExist(ss, cPath.TYPE_DIR):
			print "Dir /etc "+ss+" exists"
		else:
			print "Dir /etc "+ss+" doesn't exist"
	#check subfile existence
	for ff in subDir:
		if thisDir.subExist(ff, cPath.TYPE_FILE):
			print "File /etc "+ff+" exists"
		else:
			print "File /etc "+ff+" doesn't exist"
	for ff in thisDir.getSubFiles():
		print ff
