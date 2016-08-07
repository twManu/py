#!/usr/bin/python
#

import os, sys, re, argparse, glob
#sys.path.append("path")
sys.path.append("./path")
sys.path.append("../basic")
from libPath import cPath


class cDiff(cPath):
	def __init__(self, myPath, otherPath):
		super(cDiff, self).__init__(myPath)
		self._otherPathObj=None
		if self._pathName:
			self._subFiles=self.getSubFiles()
			self._otherPathObj=cPath(otherPath)
			if self._otherPathObj:
				self._otherPathName=self._otherPathObj.getPath()
				if not self._otherPathName:
					self._otherPathObj=None

	#Return path object of the other path
	def getOtherObj(self):
		return self._otherPathObj

# main
#
if __name__ == '__main__':
	obj=cDiff("~/work/sdk-2.0.2.11/filesystem/lib",
		"~/work/sdk-2.0.2.11/linux-devkit/sysroots/cortexa15hf-vfp-neon-linux-gnueabi/lib")
	srcPath=obj.getPath()
	otherPathObj=obj.getOtherObj()
	#both path valid
	if otherPathObj and srcPath:
		for subFile in obj.getSubFiles():
			theType=obj.getType(srcPath+'/'+subFile)
			if otherPathObj.subExist(subFile, theType):
				print "common file: "+subFile
			'''
			else:
				print "Missing "+subFile+" in "+otherPath.getPath()
			'''

