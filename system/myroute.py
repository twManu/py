#!/usr/bin/python

import os, sys, re, argparse, subprocess, glob, copy


class inet(object):
	def __init__(self):
		self._intfDict={}           #interface name and ip
		self._d4GWDict={}           #default gw and interface
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

	def _prepareIntf(self):
		curIntf=''
		for line in self._cmdStdoutIter('ifconfig'):
			if re.match(r'[^\ \t]', line):
				#interface got
				line=line.strip()
				if line:
					curIntf=line.split()[0]      #can't be ''
					self._intfDict[curIntf]=""
			else:
				if re.search(r'inet addr', line):
					#ip got
					ip=line.split()[1]
					ip=ip.split(':')[1]
					self._intfDict[curIntf]=ip

	def _prepareRoute(self):
		for line in self._cmdStdoutIter('route'):
			if re.match(r'default', line):
				words=line.split()
				self._d4GWDict[words[7]]=words[1]

	def getIntf(self):
		return copy.deepcopy(self._intfDict)

	def getRoute(self):
		return copy.deepcopy(self._d4GWDict)
	#route add -net 10.3.0.0 netmask 255.255.254.0 gw 10.3.57.254
	#route del -net 10.3.0.0 netmask 255.255.254.0


obj=inet()
print 'interface:'
for intf, ip in obj.getIntf().iteritems():
	print intf, ip

print '\ndefault gateway:'
for intf, ip in obj.getRoute().iteritems():
	print intf, ip
