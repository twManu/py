#!/usr/bin/python

import os, sys, re, argparse, subprocess, glob, copy
sys.path.append('../basic')
from lib import manuLib



class packet(object):
	PKT_BASIC="vim ssh synaptic dos2unix gitk"
	PKT_DEV="g++ build-essential meld minicom libpython-dev"
	PKT_DEVNET="tftpd-hpa nfs-common nfs-kernel-server openssh-server"
	PKT_NET="filezilla"
	PKT_FCITX="cmake fcitx-libs-dev fcitx-tools fcitx-table"
	ALL_PKT=(PKT_BASIC, PKT_DEV, PKT_DEVNET, PKT_NET, PKT_FCITX)
	def __init__(self):
		self._install=self.PKT_BASIC


class apt(object):
	def __init__(self):
		self._lib=manuLib()
		self._isRoot=False
		if self._lib.isRoot():
			self._isRoot=True
		self._pkt=packet() 

	# Return interface dictionary and optionally print the message
	# In  : prnt - whether to print the message
	# Ret : a dict object w/ keys of interface name
	def getInfo(self):
		for sets in self._pkt.ALL_PKT:
			if sets:
				print sets


#main
if __name__ == '__main__':
	def check_param():
        	parser = argparse.ArgumentParser()
	        parser.add_argument('-q', action='store_true', dest='query', default=False,
        	        help='query package and installation')
	        arg=parser.parse_args()
        	return arg

	arg=check_param()
	obj=apt()
	if arg.query:
		obj.getInfo()
	else:
		obj.getInfo()

