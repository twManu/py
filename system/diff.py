#!/usr/bin/python
#

import os, sys, re, argparse, glob
#sys.path.append("path")
sys.path.append("./path")
sys.path.append("../basic")
from libPath import cPath


class cDiff(cPath):
	# myPath is source that other might link to
	def __init__(self, myPath, otherPath, debug=False):
		super(cDiff, self).__init__(myPath, False)
		self._otherPathObj=None
		self._linkAppend=""
		self._debug=debug
		if self._pathName:
			#self._subFiles=self.getSubFiles()
			self._otherPathObj=cPath(otherPath)
			if self._otherPathObj:
				self._otherPathName=self._otherPathObj.getPath()
				if not self._otherPathName:
					self._otherPathObj=None
				else:
					self._findLinkAppend()

	def _debug(self, msg=""):
		if self._debug: print msg
			
	# call after both path are valid
	# Out : _linkAppend updated
	def _findLinkAppend(self):
		if self._linkAppend:
			return
		tmp1=self._pathName
		tmp2=self._otherPathObj.getPath()
		print "Checking "+tmp1+" against "+tmp2
		while not re.match(tmp2, tmp1):
			tmp2=os.path.dirname(tmp2)
			if tmp2 == "/":
				print "  Match at root"
				break
			self._linkAppend += "../"
		
	def getLinkAppend(self):
		return self._linkAppend


	def _findSo1(self):
		totalSize=0
		oPath=self._otherPathObj.getPath()
		for ff in self.getSubFiles():
			self._DBG("")
			fname1=self._pathName+ff
			self._DBG(fname1, False)
			if not os.path.isfile(fname1): continue
			self._DBG(' a file', False)
			fsize=os.path.getsize(fname1)
			if fsize < 4000: continue
			self._DBG(' large size', False)
			fname2=oPath+ff
			if os.path.isfile(fname2):
				self._DBG(' other', False)
				if os.path.getsize(fname2) == fsize:
					totalSize += fsize
					self._DBG(fsize)
		self._DBG("")
		self._DBG(totalSize)
			
			

	def _findSo(self, subPath):
		oPath=self._otherPathObj.getPath()
		nSubPath=re.sub(r'^/', "", subPath)
		totalSize=0
		for ff in glob.glob(self._pathName+subPath+'/*.so*'):
			if os.path.islink(ff): continue
			if os.path.isdir(ff): continue
			fsize=os.path.getsize(ff)
			if fsize < 4000: continue
			base=os.path.basename(ff)
			if os.path.exists(oPath+subPath+'/'+base):
				totalSize += fsize
				print 'ln -s '+self._linkAppend+nSubPath+'/'+base,
				print '      size= '+str(fsize)
		print 'Total size = '+str(totalSize)

	#Return path object of the other path
	def getOtherObj(self):
		return self._otherPathObj

# main
#
if __name__ == '__main__':
	dir1=cPath("~/work/aphsdk/targetNFS")
	dir2=cPath("~/work/aphsdk/linux-devkit/sysroots/cortexa15hf-neon-linux-gnueabi")
	chkPath=("/usr/lib", "/lib")
	if not dir1.getPath() or not dir2.getPath():
		print "Invalid path ... program exits"
		system.exit(1)
	obj=cDiff(dir1.getPath(), dir2.getPath(), True)
	obj._findSo1()
	'''
	for sub in chkPath:
		obj._findSo(sub)
	'''
