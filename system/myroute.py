#!/usr/bin/python

import os, sys, re, argparse, subprocess, glob, copy


class inet(object):
	INET_INTF='intf'
	INET_IP='ip'
	INET_MASK='mask'
	INET_NETWORK='network'              #to network
	INET_ROUTE='route'                  #route to gw
	def __init__(self):
		self._intfDict={}           #dict of 'name':obj and each obj is dict
		self._root=False
		self._checkRoot()
		self._prepareIntf()
		self._prepareRoute()

		
# Fork a process to execute given command. Then return the line iterator of command.
# There might be empty line returned. Use line.strip()
#
# In  : cmd - quoted command for execution
# Ret : iterator of line
	def _cmdStdoutIter(self, cmd):
		p=subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
		return iter(p.stdout.readline, '')

	def _checkRoot(self):
		for line in self._cmdStdoutIter('id'):
			if re.search('(root)', line):
				self._root=True
	
	#prepare list of dictionary and each in
	#	'intf'=eth1
	#       'ip'=172.16.210.1
	#       'mask'=255.255.255.0
	#	'default'=False
	def _prepareIntf(self):
		for line in self._cmdStdoutIter('ifconfig'):
			if re.match(r'[^\ \t]', line):
				theDict={}
				#interface got
				line=line.strip()
				if line:
					theDict[self.INET_INTF]=line.split()[0]
					theDict[self.INET_NETWORK]=''
					theDict[self.INET_MASK]=''
					theDict[self.INET_ROUTE]=''
					#print 'adding '+theDict[self.INET_INTF]
					self._intfDict[theDict[self.INET_INTF]]=theDict
			elif re.search(r'inet addr', line):
				words=line.split()
				#words[1]='addr:172.16.210.1'	
				theDict[self.INET_IP]=words[1].split(':')[1]
				if len(words) >= 4:
					#words[3]='Mask:255.255.255.0'
					theDict[self.INET_MASK]=words[3].split(':')[1]


	#need self._intfDict database created
	def _prepareRoute(self):
		for line in self._cmdStdoutIter('route'):
			words=line.split()
			if len(words) < 8: continue
			if words[7] in self._intfDict:
				theDict=self._intfDict[words[7]]
				#print 'adding '+theDict[self.INET_INTF], words[0]
				if 'default' == words[0]:
					theDict[self.INET_ROUTE]=words[1]
					theDict[self.INET_NETWORK]='0.0.0.0'
				else:
					theDict[self.INET_NETWORK]=words[0]


	#def getRoute(self):
	#	return copy.deepcopy(self._d4GWDict)
	#route add -net 10.3.0.0 netmask 255.255.254.0 gw 10.3.57.254
	#route del -net 10.3.0.0 netmask 255.255.254.0

	#get information
	def getInfo(self, prnt=False):
		ignorePrefix=('lo', 'virbr', 'vmnet')
		for intf in self._intfDict:
			item = self._intfDict[intf]
			print item[self.INET_INTF],
			if item[self.INET_ROUTE]:
				print item[self.INET_ROUTE],
			else:
				print '*', 
			print item[self.INET_NETWORK], item[self.INET_MASK]


obj=inet()
obj.getInfo()

