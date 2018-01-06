#!/usr/bin/python

import fcntl, os, sys, struct, argparse
from v4l2_def import *


class video:
        #init device
	# node - 'videoX'
	# verbose - debug level, 0, 1, 2
        def __init__(self, node='video0', verbose=0):
                self._fd = None
                self._path='/dev/'+node
                self._cap = None
		self._dictFmt = {}          #dict of emulated format list for each type
		self._dictFrmSz = {}        #dict of emulated format list for each pix format
		self._verbose = verbose
                #exist?
                if not os.path.exists(self._path):
                        print 'Missing '+self._path
                        self._path = None
                        return
                #can open?
                try:
                        self._fd = open(self._path, "wb")
                        print self._path + " open successful"
                except:
                        print 'Fail to open '+self._path
                        self._fd = None
                        self._path = None


	# given format, return its name
	def _nameOfDictByValue(self, dictObj, value):
		for kk, vv in dictObj.iteritems():
			if vv == value:
				return kk
		return 'unknown format'


	# Show format name
	# In  : capType - 0 means not to show title and type
	#               - otherwise show title in advance
	def _showFmt(self, fmt, capType):
		if capType>=0:
			print "Format of "+self._nameOfDictByValue(g_V4L2_BUF_TYPE, capType)+':'
		print '\t'+self._nameOfDictByValue(g_V4L2_PIX_FMT, fmt[v4l2_fmtdesc4_pixelformat])


        # In  : enumType - type of format to enumerate, see g_V4L2_BUF_TYPE
	# In  : _verbose - debug level
	#         0: none
	#         1: success
	#         2: struct
        # Ret : capability unpacked
        def enumfmt(self, capType=V4L2_BUF_TYPE_VIDEO_CAPTURE):
                if not self._fd:
                        return None
		#check device support
		if V4L2_BUF_TYPE_VIDEO_CAPTURE == capType and\
		   not self._cap[v4l2_capability4_capabilities] & V4L2_CAP_VIDEO_CAPTURE:
			if self._verbose:
				print capType, 'is not supported'
			return None
		#create if not yet
                if not capType in self._dictFmt:
			self._dictFmt[capType] = []
			index = 0
			while True:
				efmt = struct.pack(v4l2_fmtdesc_formatString\
					, index, capType, 0, '', 0, 0, 0, 0, 0)
                        	try:
                                	ret = struct.unpack(v4l2_fmtdesc_formatString\
						, fcntl.ioctl(self._fd, VIDIOC_ENUM_FMT, efmt))
					if self._verbose:
						if 2 <= self._verbose:
							print 'got enum fmt '+ret[v4l2_fmtdesc3_description]
						if not index:
							self._showFmt(ret, capType)
						else:
							self._showFmt(ret, -1)
					self._dictFmt[capType].append(ret[v4l2_fmtdesc4_pixelformat])
					self.enumFrameSz(ret[v4l2_fmtdesc4_pixelformat])
					index += 1
				except:
					if not index and self._verbose:
						print 'fail to enum fmt'
                                	break
                return self._dictFmt[capType]


	# frmSz is packed
	def _showFrmSz(self, frmSz):
		print '\t\t'+self._nameOfDictByValue(g_V4L2_FRMIVAL, frmSz[v4l2_frmsizeenum2_type])+' : (',
		if frmSz[v4l2_frmsizeenum2_type] == V4L2_FRMIVAL_TYPE_DISCRETE:
			#width x height
			print frmSz[v4l2_frmsizeenum3_min_width],
			print 'x',
			print frmSz[v4l2_frmsizeenum4_max_width],
			print ')'
		elif frmSz[v4l2_frmsizeenum2_type] == V4L2_FRMIVAL_TYPE_CONTINUOUS:
			print frmSz[v4l2_frmsizeenum3_min_width],
			print 'x',
			print frmSzret[v4l2_frmsizeenum4_max_width],
			print ') ... (',
			print frmSz[v4l2_frmsizeenum6_min_height],
			print 'x',
			print frmSz[v4l2_frmsizeenum7_max_height],
			print ')'
		elif frmSz[v4l2_frmsizeenum2_type] == V4L2_FRMIVAL_TYPE_STEPWISE:
			print frmSz[v4l2_frmsizeenum3_min_width],
			print 'x'
			print frmSz[v4l2_frmsizeenum4_max_width],
			print '+ ',
			print frmSz[v4l2_frmsizeenum5_step_width],
			print ') ... (',
			print frmSz[v4l2_frmsizeenum6_min_height],
			print 'x',
			print frmSz[v4l2_frmsizeenum7_max_height],
			print '+',
			print frmSz[v4l2_frmsizeenum8_step_height],
			print ')'
		else:
			print 'invalid type'


	# In  : pformat - pixel format
	#       wxh - tuple of (width, height)
	#       _dictFrmSz - data base of frame support
	def _printFramerate(self, pformat, wxh):
		if self._dictFrmSz and pformat in self._dictFrmSz and \
		   wxh in self._dictFrmSz[pformat] and 'rate' in self._dictFrmSz[pformat][wxh]:
			index = 0
			for rr in self._dictFrmSz[pformat][wxh]['rate']:
				if not index:
					print('\t\t   %d/%d' % rr),
				else:
					print(',%d/%d' % rr),
				index += 1
			print


	# check frame interval supported by given format/w/h
	# pformat/width/height - pix format/width/height
	# 
	def enumFrameIval(self, pformat, width, height):
		if not self._fd:
                        return None
		index = 0
		#make sure list created
		if not 'rate' in self._dictFrmSz[pformat][(width, height)]:
			self._dictFrmSz[pformat][(width, height)]['rate'] = []
		#print 'checking interval', pformat, width, height
		while True:
			efrmIval = struct.pack(v4l2_frmivalenum_formatString, index, pformat, width, height, 0, 0\
				, 0, 0, 0)
                       	try:
				ret = fcntl.ioctl(self._fd, VIDIOC_ENUM_FRAMEINTERVALS, efrmIval)
			except:
				if not index and self._verbose:
					print 'fail to enum frame interval'
				break
			efrmIval = struct.unpack(v4l2_frmivalenum_formatString, ret)
			#todo hard coding 1=descrete
			if efrmIval[v4l2_frmivalenum4_type] != 1:
				print 'interval type for', pformat, width, height, ' not supported'
			else:
				framerate = ( efrmIval[v4l2_frmivalenum5_numerator], efrmIval[v4l2_frmivalenum6_denominator] )
				self._dictFrmSz[pformat][(width, height)]['rate'].append( framerate )
			index += 1


	# check frame size supported by given format
	# pformat - pix format
	#
	def enumFrameSz(self, pformat):
		if not self._fd:
                        return None
		if not pformat in self._dictFrmSz:
			self._dictFrmSz[pformat] = {}               #each is of key (w,h)
			#print 'creating', pformat
			index = 0
			while True:
				'''
				efrmsz = struct.pack(v4l2_frmsizeenum_formatString0, index, pformat, 0, 0, 0)
                        	try:
                               		ret = fcntl.ioctl(self._fd, VIDIOC_ENUM_FRAMESIZES, efrmsz)
				except:
					if not index:
						print 'fail to enum frame size'
                               		break
				efrmsz = struct.unpack(v4l2_frmsizeenum_formatString0, ret)
				if ret[v4l2_frmsizeenum2_type] != V4L2_FRMIVAL_TYPE_DISCRETE:
				'''
				efrmsz = struct.pack(v4l2_frmsizeenum_formatString, index, pformat, 0, 0, 0\
						, 0, 0, 0, 0, 0, 0)
                        	try:
                               		ret = fcntl.ioctl(self._fd, VIDIOC_ENUM_FRAMESIZES, efrmsz)
				except:
					if not index and self._verbose >= 2:
						print 'fail to enum frame size 2'
					break
				efrmsz = struct.unpack(v4l2_frmsizeenum_formatString, ret)
				w = efrmsz[v4l2_frmsizeenum3_min_width]
				h = efrmsz[v4l2_frmsizeenum4_max_width]
				if (w, h) in self._dictFrmSz[pformat]:
					print 'Duplicated frame size', w, 'x', h, '... ignored !!!!'
					continue
				self._dictFrmSz[pformat][(w, h)] = {}     #each is of key 'struct' and 'rate'
				self._dictFrmSz[pformat][(w, h)]['struct'] = efrmsz
				self.enumFrameIval(pformat, w, h)
				if self._verbose:
					self._showFrmSz(efrmsz)
					if self._verbose >= 2:
						self._printFramerate(pformat, (w, h))
				index += 1
                return self._dictFrmSz


	def printCap(self):
		if not self._cap:
			return
		print self._cap[v4l2_capability1_card]+':'
		print '\tbacked by ' + self._cap[v4l2_capability0_driver],
		print '@ '+self._cap[v4l2_capability2_bus_info]
		#capabilities
		if self._cap[v4l2_capability4_capabilities]:
			print 'Capabilities:'
			for key in g_V4L2_CAP:
				if self._cap[v4l2_capability4_capabilities] & g_V4L2_CAP[key]:
					print '\t'+key

	# In  : _verbose - debug level
	#         0: none
	#         1: success
	#         2: struct
	# OUt : _cap - capability structure
	# Ret : capability unpacked
        def querycap(self):
		if not self._fd:
			return None
		if self._cap:
			return self._cap
		cap = struct.pack(v4l2_capability_formatString, '', '', '', 0, 0, 0, 0, 0, 0)
		try:
			cap = fcntl.ioctl(self._fd, VIDIOC_QUERYCAP, cap)
			self._cap = struct.unpack(v4l2_capability_formatString, cap)
			if self._verbose:
				if 1 == self._verbose:
					print 'VIDIOC_QUERYCAP successful'
				else:
					self.printCap()
		except:
			print "VIDIOC_QUERYCAP failure"
			return None
		return self._cap


        def __exit__(self):
                if self._fd:
                        print "Exit "+self._path
                        close(self._fd)
                        self._fd = None

        def __close__(self):
                if self._fd:
                        print "Closing "+self._path
                        close(self._fd)
                        self._fd = None



#main
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', type=int, action='store', dest='verbose', default=0,
		choices=[0, 1, 2])
	parser.add_argument('-d', type=int, action='store', default=0,
		dest='DEV_NR', help='it stands for /dev/video[DEV_NR]')
	args = parser.parse_args()
	dev = video('video'+str(args.devNr), args.verbose)
        dev.querycap()
	dev.enumfmt()

