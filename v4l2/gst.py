#!/usr/bin/python

import fcntl, os, sys, struct, argparse, commands, re
from v4l2_def import *

class gst(object):
	gstCmd = ('gst-launch-1.0',)
	dictPipeType = {
		'case1': {
			  'must': ('src', 'sink')
			, 'option': ('src', 'srcFormat', 'decode', 'encode', 'sinkFormat', 'sink')
		}
	}
        #
	# verbose - debug level, 0, 1, 2
        def __init__(self, verbose=0):
		self._verbose = verbose
		self._pipe = ''
		hasGst = None
		for self._gstCmd in self.gstCmd:
			if verbose>=2:
				print 'checking', self._gstCmd
			hasGst = commands.getoutput(self._gstCmd)
			if hasGst: break
		if not hasGst:
			print 'Fails to find gst command'
			sys.exit(-1)
		elif verbose:
			print 'Using '+self._gstCmd


	# check if provided graph violate the rule
	# dictGraph - dict in {
	#	'case': <case string>
	#	'<option1>: string1
	#	'<option2>: string2
	#	:
	# }
	# In  : _graph
	#       _graph['case'] must be in one of the key in dictPipeType
	# Ret : True - success
	#       False - failure
	def build(self, dictGraph):
		#check case
		if not 'case' in dictGraph:
			if self._verbose:
				print 'Missing case string in graph'
			return False
		if dictGraph['case'] in self.dictPipeType:
			case = self.dictPipeType[dictGraph['case']]
			if self._verbose:
				print 'in', dictGraph['case']
		else:
			if self._verbose:
				print 'unknown case of graph'
			return False
		#check must
		for must in case['must']:
			if not must in dictGraph:
				if self._verbose:
					print 'Missing', must
				return False
		#build pipe
		self._pipe = ''
		for option in case['option']:
			if option in dictGraph:
				if self._pipe:
					self._pipe += ' !'
				self._pipe += dictGraph[option]
		if self._verbose:
			print 'pipe =', self._pipe
		return True


	#run the pipe
	def run(self):
		if self._pipe:
			cmd = self._gstCmd+' '+self._pipe
			print cmd
			commands.getoutput(cmd)

class gstv4l2(gst):
	supportFmt = (V4L2_PIX_FMT_MJPEG, V4L2_PIX_FMT_YUYV, V4L2_PIX_FMT_H264)
	def __init__(self, verbose):
		super(gstv4l2, self).__init__(verbose)
		self.setParam(devnr=0, fmt=V4L2_PIX_FMT_MJPEG, w=1920, h=1080, raten=30, rated=1)
		self._devnr = 0


	# foramt, width, height, rate_num, rate_denom
	# fmt 
	def setParam(self, devnr=None, fmt=None, w=None, h=None, raten=None, rated=None):
		if not fmt in self.supportFmt:
			print 'Unsupport format', fmt
			return False
		if devnr: self._devnr = devnr
		if fmt: self._format = fmt
		if w: self._width = w
		if h: self._height = h
		#framerate inverse of interval
		if raten: self._rate_num = raten
		if rated: self._rate_denom = rated
		return True

	def build(self):
		graph = {
			V4L2_PIX_FMT_MJPEG: {
				  'case': 'case1'
				, 'src': 'v4l2src device=/dev/videoDEVNR do-timestamp=true'
				, 'srcFormat': 'image/jpeg, width=WIDTH, height=HEIGHT, framerate=RATEN/RATED'
				, 'decode': 'jpegparse ! jpegdec'
				, 'sinkFormat': 'videoconvert'
				, 'sink': 'xvimagesink sync=false'
			},
			V4L2_PIX_FMT_YUYV: {
				  'case': 'case1'
				, 'src': 'v4l2src device=/dev/videoDEVNR do-timestamp=true'
				, 'srcFormat': 'video/x-raw, width=WIDTH, height=HEIGHT, framerate=RATEN/RATED'
				, 'sinkFormat': 'videoconvert'
				, 'sink': 'xvimagesink sync=false'
			},
			V4L2_PIX_FMT_H264: {
				  'case': 'case1'
				, 'src': 'v4l2src device=/dev/videoDEVNR do-timestamp=true'
				, 'srcFormat': 'video/x-h264, width=WIDTH, height=HEIGHT, framerate=RATEN/RATED'
				, 'decode': 'h264parse ! avdec_h264'
				, 'sinkFormat': 'videoconvert'
				, 'sink': 'xvimagesink sync=false'
			}
		}
		if not self._format in graph:
			print 'unsupport format'
			return False
		dict = graph[self._format]
		dict['src'] = re.sub('DEVNR', str(self._devnr), dict['src'])
		dict['srcFormat'] = re.sub('WIDTH', str(self._width), dict['srcFormat'])
		dict['srcFormat'] = re.sub('HEIGHT', str(self._height), dict['srcFormat'])
		dict['srcFormat'] = re.sub('RATEN', str(self._rate_num), dict['srcFormat'])
		dict['srcFormat'] = re.sub('RATED', str(self._rate_denom), dict['srcFormat'])
		return super(gstv4l2, self).build(dict)



#main
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', type=int, action='store', dest='verbose', default=0,
		choices=[0, 1, 2, 3])
	parser.add_argument('-d', type=int, action='store', dest='devnr', default=0)
	parser.add_argument('-W', type=int, action='store', dest='width', default=0)
	parser.add_argument('-H', type=int, action='store', dest='height', default=0)
	parser.add_argument('-N', type=int, action='store', dest='numerator', default=0)
	parser.add_argument('-D', type=int, action='store', dest='denominator', default=0)
	helpStr=''
	index = 0
	for fmt in gstv4l2.supportFmt:
		helpStr += str(index) + ' :' + nameOfDictByValue(g_V4L2_PIX_FMT, fmt)
		index += 1
		if index != len(gstv4l2.supportFmt):
			helpStr += ', '
	parser.add_argument('-f', type=int, action='store', dest='format', default=0,
		choices=[0, 1, 2], help=helpStr)
	args = parser.parse_args()
	obj = gstv4l2(args.verbose)
	obj.setParam(
		devnr=args.devnr,
		fmt=gstv4l2.supportFmt[args.format],
		w=args.width,
		h=args.height,
		raten=args.numerator,
		rated=args.denominator)
	if obj.build():
		obj.run()
