#!/usr/bin/python

import fcntl, os, sys, struct
from v4l2_def import *


class video:
        #init device
        def __init__(self, node='video0'):
                self._fd = None
                self._path='/dev/'+node
                self._cap = None
		self._dictFmt = {}          #dict of emulated format list for each type
		self._dictFrmSz = {}        #dict of emulated format list for each pix format
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
	#       show - to show info or not
        # Ret : capability unpacked
        def enumfmt(self, capType=V4L2_BUF_TYPE_VIDEO_CAPTURE, show=False):
                if not self._fd:
                        return None
		#check device support
		if V4L2_BUF_TYPE_VIDEO_CAPTURE == capType and\
		   not self._cap[v4l2_capability4_capabilities] & V4L2_CAP_VIDEO_CAPTURE:
			if show:
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
					#print 'got enum fmt '+ret[v4l2_fmtdesc3_description]
					if show:
						if not index:
							self._showFmt(ret, capType)
						else:
							self._showFmt(ret, -1)
					self._dictFmt[capType].append(ret[v4l2_fmtdesc4_pixelformat])
					self.enumFrameSz(ret[v4l2_fmtdesc4_pixelformat])
					index += 1
				except:
					if not index:
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
			print frmSz[v4l2_frmsizeenum3_min_height],
			print 'x',
			print frmSz[v4l2_frmsizeenum4_max_height],
			print ')'
		elif frmSz[v4l2_frmsizeenum2_type] == V4L2_FRMIVAL_TYPE_STEPWISE:
			print frmSz[v4l2_frmsizeenum3_min_width],
			print 'x'
			print frmSz[v4l2_frmsizeenum4_max_width],
			print '+ ',
			print frmSz[v4l2_frmsizeenum5_step_width],
			print ') ... (',
			print frmSz[v4l2_frmsizeenum3_min_height],
			print 'x',
			print frmSz[v4l2_frmsizeenum4_max_height],
			print '+',
			print frmSz[v4l2_frmsizeenum8_step_height],
			print ')'
		else:
			print 'invalid type'


	# check frame size supported by given format
	# pformat - pix format
	#
	def enumFrameSz(self, pformat):
		if not self._fd:
                        return None
		if not pformat in self._dictFrmSz:
			self._dictFrmSz[pformat] = []
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
				if True:
					efrmsz = struct.pack(v4l2_frmsizeenum_formatString, index, pformat, 0, 0, 0\
							, 0, 0, 0, 0, 0, 0)
	                        	try:
	                               		ret = fcntl.ioctl(self._fd, VIDIOC_ENUM_FRAMESIZES, efrmsz)
					except:
						if not index:
							print 'fail to enum frame size 2'
						break
					efrmsz = struct.unpack(v4l2_frmsizeenum_formatString, ret)
				self._showFrmSz(efrmsz)
				self._dictFrmSz[pformat].append(efrmsz)
				index += 1
                return self._dictFrmSz

	# In  : show - to show info or not
	# OUt : _cap - capability structure
	# Ret : capability unpacked
        def querycap(self, show=False):
		if not self._fd:
			return None
		if self._cap:
			return self._cap
		cap = struct.pack(v4l2_capability_formatString, '', '', '', 0, 0, 0, 0, 0, 0)
		try:
			cap = fcntl.ioctl(self._fd, VIDIOC_QUERYCAP, cap)
			self._cap = struct.unpack(v4l2_capability_formatString, cap)
			if not show:
				print 'VIDIOC_QUERYCAP successful'
			else:
				print self._cap[v4l2_capability1_card]+':'
				print '\tbacked by ' + self._cap[v4l2_capability0_driver],
				print '@ '+self._cap[v4l2_capability2_bus_info]
				#capabilities
				if self._cap[v4l2_capability4_capabilities]:
					print 'Capabilities:'
					for key in g_V4L2_CAP:
						if self._cap[v4l2_capability4_capabilities] & g_V4L2_CAP[key]:
							print '\t'+key
		except:
			print "failure"
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
	dev = video('video0')
        dev.querycap(show=True)
	dev.enumfmt(show=True)

