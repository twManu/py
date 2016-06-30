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

	# del the gateway according to database
	# Ret : False - not a root
	#       True - do as a root
	def delDefaultGW(self):
		if not self._root:
			print "Need to be a root for the task"
			return False
		else:
			for intf in self._intfDict:
				item = self._intfDict[intf]
				if item[self.INET_ROUTE]:
					print "Deleting "+item[self.INET_ROUTE]
					os.system('route del default gw '+item[self.INET_ROUTE])
		return True


	# Get default gateway from database by given network
	# In  : network - the a.b.c.d network
	# Ret : '' - not in database
	#       otherwise - of gateway string
	def _getDefaultGW(self, network):
		defaultGW={
			  '10.3.56.0' : '10.3.57.254'
			, '192.168.42.0' : '192.168.42.129'
		}
		if network in defaultGW:
			return defaultGW[network]
		return ''


	# add a gateway according to database
	# In  : intf - interface name
	#       gw - gateway, if not provided, xx.xx.xx.254 used
	# Ret : False - not a root or invalid argument
	#       True - do as a root
	def addDefaultGW(self, intf, gw=''):
		if not self._root:
			print "Need to be a root for the task"
		elif not intf in self._intfDict:
			print "Invalid interface "+intf
		else:
			item = self._intfDict[intf]
			mask = item[self.INET_MASK]
			if not mask:
				print "Fail to get network mask"
				return False
			#
			#determine gw
			#
			if not gw:
				gw = self._getDefaultGW(item[self.INET_NETWORK])
			if not gw:
				ips=item[self.INET_NETWORK].split('.')
				masks=mask.split('.')
				for i in range(0, 4):
					thisIP=int(ips[i])&int(masks[i])
					if not gw:
						gw=str(thisIP)
					elif not thisIP:
						gw+=".0"
					else:
						gw+="."+str(thisIP)
			item[self.INET_ROUTE]=gw
			print "Adding GW "+item[self.INET_ROUTE]
			os.system('route add default gw '+item[self.INET_ROUTE])
			return True
		return False


	# Return interface dictionary and optionally print the message
	# In  : prnt - whether to print the message
	# Ret : a dict object w/ keys of interface name
	def getInfo(self, prnt=False):
		ignorePrefix=('lo', 'virbr', 'vmnet')
		if prnt:
			for intf in self._intfDict:
				item = self._intfDict[intf]
				print item[self.INET_INTF],
				if item[self.INET_ROUTE]:
					print item[self.INET_ROUTE],
				else:
					print '*', 
				print item[self.INET_NETWORK], item[self.INET_MASK]
		return copy.deepcopy(self._intfDict)


#main
if __name__ == '__main__':
	def check_param():
        	parser = argparse.ArgumentParser()
	        parser.add_argument('-g', action='store', dest='newGW', default='',
        	        help='set new <interfacce>[:gateway]... should be done by root')
	        arg=parser.parse_args()
        	return arg

	arg=check_param()
	obj=inet()
	if arg.newGW:
		#obj.getInfo()
		words=arg.newGW.split(':')
		if not obj.delDefaultGW():
			sys.exit()
		if len(words)>=2:
			obj.addDefaultGW(words[0], words[1])
		else:
			obj.addDefaultGW(words[0])
	else:
		obj.getInfo(True)

