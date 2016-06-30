#!/usr/bin/python

import sys, re, os
import argparse

sys.path.append('../../basic')
from lib import manuLib

INT_INTF='enp3s0'
INT_GW='10.3.57.254'
#tuple of dictionary
INT_NET=(
		  {
			'net': '10.0.0.0',
			'mskLen': 8
		}
		, {
			'net': '172.0.0.0',
			'mskLen': 8
		}
)

class routing(manuLib):
	# In  : intf - net device
	def __init__(self, intf=None):
		super(routing, self).__init__()
		self._intf=intf

	# form "a.b.c.d/mask-length" from rule dictionary
	# Ret : "a.b.c.d/mask-length"
	def _ruleStr(self, aRule):
		return aRule['net']+"/"+str(aRule['mskLen'])


	# Check if the rule netRule already exists
	#
	# In  : netRule is a net/mskLen dictionary describing the rule
	#       None - means print routing rules
	# Ret : True - existing
	#       False - otherwise
	def _ruleExisting(self, netRule=None):
		cmpStr=""
		if netRule: cmpStr=self._ruleStr(netRule)
		for curRule in self.cmdOutput('ip route'):
			if cmpStr:
				word0=curRule.split()[0]
				if cmpStr==word0:
					return True
			else:
				line=curRule.strip()
				if line:
					print line
		return False


	# Check if the ipMsk already exists
	#
	# In  : ipMsk - a.b.c.d or a.b.c.d/n
	# Ret : True - existing
	#       False - otherwise
	def _ipMskStrExisting(self, ipMsk):
		for curRule in self.cmdOutput('ip route'):
			word0=curRule.split()[0]
			if ipMsk==word0: return True
		return False


	# add or delete rules routing internally
	# In  : onoff - True : add
	#               False: del
	def intRoute(self, onoff, gw=INT_GW):
		if not self._intf:
			return
		for rule in INT_NET:
			ipMsk=self._ruleStr(rule)
			exist=self._ruleExisting(rule)
			if onoff:                #add
				if exist:
					print ipMsk+" already exists ...ignore"
					continue
				cmd = "ip route add "+ipMsk
				cmd += " dev "+self._intf+" via "+gw
			else:
				if not exist:
					print ipMsk+" not in routing table"
					continue
				cmd = "ip route del "+ipMsk
			os.system(cmd)


	# delete a routing rule
	# In  : ipMsk - a.b.c.d/maskLen or a.b.c.d
	def delRoute(self, ipMsk):
		if not self. _ipMskStrExisting(ipMsk):
			print ipMsk+' doesn\'t exist in rule'
		cmd = "ip route del "+ipMsk
		os.system(cmd)


	# print all routing info	
	def showRoute(self):	
		self._ruleExisting()
		


#
# main
#
if __name__ == '__main__':
	def getParam():
		parser=argparse.ArgumentParser()
		parser.add_argument('-s', action='store_true', dest='show_route', default=False,
			help='show routings')
		parser.add_argument('-i', action='store', dest='internal_on', default=0,
			help='1: add rules, otherwise: del rules')
		parser.add_argument('-d', action='store', dest='interface', default=INT_INTF,
			help='the network interface to do with')
		parser.add_argument('-D', action='store', dest='del_net', default="",
			help='the network to delete')
		arg = parser.parse_args()
		return arg

	arg=getParam()
	if arg.show_route:
		route=routing()
		#print rules
		route.showRoute()
		sys.exit(0)

	route=routing(arg.interface)
	if not route.isRoot():
		print "Need to be a root"
		sys.exit(1)
	#do according to internal table
	if arg.internal_on:
		print "value is "+arg.internal_on
		route.intRoute('1'==arg.internal_on)
	elif arg.del_net:
		route.delRoute(arg.del_net)

