#!/usr/bin/python

import commands, re, sys, os, argparse
from time import sleep

#git hub as key wo git@10.3.58.47:
#aten git as value wo manuchen@git.aten.com:
g_git_pair = {
	  "manuchen/gst-plugins-good-1.6.3.git": "/repo/module/am57_gst-plugins-good-1.6.3"
	, "system/sitara_uboot.git": "/repo/module/am57_uboot"
	, "kernel/sitara_kernel44.git": "/repo/module/am57_kernel44"
	, "kernel/tools.git": "/repo/module/am57_mediaEngine"
	, "system/system_tool.git": "/repo/module/am57_systool"
	, "system/post_aphsdk.git": "/repo/module/am57_aphsdk"
	, "manuchen/weston.git": "/repo/module/am57_weston"
	, "manuchen/util.git": "/repo/module/am57_util"
}

g_debug=False
#g_debug=True

def cmdExec(cmd):
	if g_debug:
		print cmd
	else:
		print '*****',
		print cmd,
		print '*****'
		os.system(cmd)

def clone(name):
	for key in g_git_pair:
		if not re.search(name, key):
			continue
		cmd = 'rm -rf '+name
		cmdExec(cmd)
		cmd = 'git clone --bare --mirror git@10.3.58.47:'+key
		cmdExec(cmd)
		cmd = 'cd '+key.split('/')[1]
		cmd += '; git remote set-url --push origin manuchen@git.aten.com:'+g_git_pair[key]
		cmd += '; git fetch -p origin'
		cmd += '; git push --mirror'
		cmdExec(cmd)
		return

clone('gst-plugins-good-1.6.3.git')
