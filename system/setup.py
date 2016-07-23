#!/usr/bin/python

import os, sys, re, argparse, subprocess, glob, copy
sys.path.append('../basic')
from lib import manuLib



class packet(object):
	PKT_BASIC="vim ssh synaptic dos2unix git"
	PKT_DEV="g++ build-essential gitk meld minicom"
	PKT_DEVNET="tftpd-hpa nfs-common nfs-kernel-server"
	PKT_NET="filezilla"
	PKT_FCITX="cmake fcitx-libs-dev fcitx-tools fcitx-table"
	ALL_PKT=(PKT_BASIC, PKT_DEV, PKT_DEVNET, PKT_NET, PKT_FCITX)
	def __init__(self):
		self._install=self.PKT_BASIC


class apt(object):
	def __init__(self):
		self._lib=manuLib()
		if not self._lib.isRoot():
			print "Installer must be run as root"
			sys.exit(1)
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
	        parser.add_argument('-i', action='store_true', dest='info', default=False,
        	        help='information')
	        arg=parser.parse_args()
        	return arg

	arg=check_param()
	obj=apt()
	if arg.info:
		obj.getInfo()
	else:
		obj.getInfo()

