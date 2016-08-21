#!/usr/bin/python

import sys, re, os
import argparse

sys.path.append('../../basic')
from lib import manuLib

INT_INTF='enp3s0'
INT_GW='10.3.57.254'
#tuple of dictionary
#the rule to be added when internal enabled
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

#the rule to be deleted when internal enabled
INT_DEL_NET=(
	  {
		'net': '10.0.1.24',
		'Iface': 'enp3s0',
		'cmd' : "route del 10.0.1.24 dev enp3s0"
	}
	, {
		'net': '10.3.56.0',
		'Iface': 'enp3s0',
		'cmd' : "ip route del 10.3.56.0/23"
	}
)


class routing(manuLib):
	# colloect 'route -n' into a dictionary
	# Ret : list of dictionary
	def _curRoute(self):
		routeList=[]
		start=False
		for line in self.cmdOutput('route -n'):
			theDict={}
			#skip processing until 'Destination' found
			if not start:
				if re.match('Destination ', line):
					start=True
				continue
			words=line.split()
			#Destination Gateway Genmask Flags Metric Ref Use Iface
			theDict['Destination']=words[0].strip()
			theDict['Gateway']=words[1].strip()
			theDict['Genmask']=words[2].strip()
			theDict['Iface']=words[7].strip()
			routeList.append(theDict)
		return routeList
	

	# In  : intf - net device
	def __init__(self, intf=None):
		super(routing, self).__init__()
		self._intf=intf
		self._curRouteList=self._curRoute()

	# form "a.b.c.d/mask-length" from rule dictionary
	# Ret : "a.b.c.d/mask-length"
	def _ruleStr(self, aRule):
		return aRule['net']+"/"+str(aRule['mskLen'])


	# Check if the rule netRule already exists
	#
	# In  : netRule is a net/mskLen dictionary describing the rule
	# Ret : True - existing
	#       False - otherwise
	def _ruleExisting(self, netRule):
		cmpStr=self._ruleStr(netRule)
		for curRule in self.cmdOutput('ip route'):
			word0=curRule.split()[0]
			if cmpStr==word0:
				return True
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
		for rule in self._curRouteList:
			if '0.0.0.0' == rule['Destination'] and\
			   INT_GW == rule['Gateway']:
				os.system('route del default gw '+INT_GW)
			for del_rule in INT_DEL_NET:
				if del_rule['net'] == rule['Destination'] and\
				   del_rule['Iface'] == rule['Iface']:
					os.system(del_rule['cmd'])
					


	# delete a routing rule
	# In  : ipMsk - a.b.c.d/maskLen or a.b.c.d
	def delRoute(self, ipMsk):
		if not self. _ipMskStrExisting(ipMsk):
			print ipMsk+' doesn\'t exist in rule'
		cmd = "ip route del "+ipMsk
		os.system(cmd)


	# print all routing info	
	def showRoute(self):	
		for rr in self._curRouteList:
			print rr['Destination'], rr['Gateway'], rr['Genmask'], rr['Iface']


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

