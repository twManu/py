#!/usr/bin/python

import fcntl, os, sys, struct, argparse
from v4l2_def import *


# calling seq:
#	obj=contruct
#	obj.querycap()
#	obj.enumfmt()
#
# struct:
#	_dictFmt = {
#		<capture type1>: {
#			<pix fmt1>: {
#				'struct' : <format1 structure>
#				'frame size1' : {
#					'struct' : <frame size1 structure>
#					'rate' : [ framerate1, framerate2, ... ]
#				}
#				'frame size2' : {
#					'struct' : <frame size2 structure>
#					'rate' : [ framerate1, framerate2, ... ]
#				}
#				:
#			}
#			<pix fmt2>: {
#				'struct' : <format1 structure>
#				'frame size1' : {
#					'struct' : <frame size1 structure>
#					'rate' : [ framerate1, framerate2, ... ]
#				}
#				'frame size2' : {
#					'struct' : <frame size2 structure>
#					'rate' : [ framerate1, framerate2, ... ]
#				}
#				:
#			}
#			:
#		}	
#		<capture type2>: {
#			<pix fmt1>: {
#				'struct' : <format1 structure>
#				'frame size1' : {
#					'struct' : <frame size1 structure>
#					'rate' : [ framerate1, framerate2, ... ]
#				}
#				'frame size2' : {
#					'struct' : <frame size2 structure>
#					'rate' : [ framerate1, framerate2, ... ]
#				}
#				:
#			}
#			:
#		}
#		:
#	}
class video:
        #init device
	# node - 'videoX'
	# verbose - debug level, 0, 1, 2
        def __init__(self, node='video0', verbose=0):
                self._fd = None
                self._path='/dev/'+node
                self._cap = None
		self._dictFmt = {}          #dict of emulated format list for each type
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


	# Show format name
	# In  : capType - 0 means not to show title and type
	#               - otherwise show title in advance
	def _showFmt(self, fmt, capType, indexHint):
		if capType>=0:
			print "Format of "+nameOfDictByValue(g_V4L2_BUF_TYPE, capType)+':'
		if indexHint >= 0:
			print '\t-F '+str(indexHint)+',',
		else:
			print '\t',
		print nameOfDictByValue(g_V4L2_PIX_FMT, fmt[v4l2_fmtdesc4_pixelformat])



        # In  : enumType - type of format to enumerate, see g_V4L2_BUF_TYPE
	#       _verbose - debug level
	#         0: none
	#         1: success
	#         2: struct
	# Out : _dictFmt[given type] created if not
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
			self._dictFmt[capType] = {}
			index = 0
			while True:
				efmt = struct.pack(v4l2_fmtdesc_formatString\
					, index, capType, 0, '', 0, 0, 0, 0, 0)
                        	try:
                                	ret = struct.unpack(v4l2_fmtdesc_formatString\
						, fcntl.ioctl(self._fd, VIDIOC_ENUM_FMT, efmt))
					if self._verbose:
						if self._verbose > 2:
							print 'got enum fmt '+ret[v4l2_fmtdesc3_description]
						if not index:
							self._showFmt(ret, capType, -1)
						else:
							self._showFmt(ret, -1, -1)
					pformat = ret[v4l2_fmtdesc4_pixelformat]
					if not pformat in self._dictFmt[capType]:
						self._dictFmt[capType][pformat] = {}
						self._dictFmt[capType][pformat]['struct'] = ret
						self._enumFrameSz(self._dictFmt[capType][pformat], pformat)
					else:
						print 'Duplicate format', nameOfDictByValue(g_V4L2_PIX_FMT, pformat)
					index += 1
				except:
					if not index and self._verbose:
						print 'fail to enum fmt'
                                	break
                return self._dictFmt[capType]

	# print result of format enumeration
	def printFmt(self):
		indexCap = 0
		for capType in self._dictFmt:
			indexFmt = 0
			hint = '-T ' + str(indexCap) + ', '
			print hint + nameOfDictByValue(g_V4L2_BUF_TYPE, capType)
			for pformat in self._dictFmt[capType]:
				self._showFmt(self._dictFmt[capType][pformat]['struct'], -1, indexFmt)
				#real g_V4L2_PIX_FMT
				self.printFramerate(self._dictFmt[capType][pformat], True, True)
				indexFmt += 1
			indexCap += 1


	# frmSz is packed
	def _showFrmSz(self, frmSz, hintIndex):
		if hintIndex >= 0:
			print '\t\t-D '+str(hintIndex)+',',
		else:
			print '\t\t',
		print nameOfDictByValue(g_V4L2_FRMIVAL, frmSz[v4l2_frmsizeenum2_type])+' : (',
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


	# In  : dictFrmSz - dictionary in
	#             [(w ,h)]['struct'] = structure from ioctl
	#             [(w ,h)]['rate'] = <list of tuple of (numerator, denominator)>
	#
	def printFramerate(self, dictFrmSz, showDetail, hint=False):
		if dictFrmSz:
			indexFrm = 0
			for wxh in dictFrmSz:
				if wxh == 'struct':
					continue
				#print V4L2_FRMIVAL_TYPE_DISCRETE : ( 800 x 600 )
				if not hint:
					indexFrm = -1
				self._showFrmSz(dictFrmSz[wxh]['struct'], indexFrm)
				if not showDetail:
					continue
				#print 1/30 ,1/24 ,1/20 ,1/15 ,1/10 ,2/15 ,1/5					
				index = 0
				for rr in dictFrmSz[wxh]['rate']:
					if not index:
						print('\t\t   %d/%d' % rr),
					else:
						print(',%d/%d' % rr),
					index += 1
				print
				indexFrm += 1


	# check frame interval supported by given format/w/h
	# dictFrmSz - dictionary of frame size we are enumerating
	# pformat/width/height - pix format/width/height
	# 
	def _enumFrameIval(self, dictFrmSz, pformat, width, height):
		if not self._fd:
                        return None
		index = 0
		#make sure list created
		if not 'rate' in dictFrmSz:
			dictFrmSz['rate'] = []
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
				dictFrmSz['rate'].append( framerate )
			index += 1


	# check frame size supported by given format
	# In  : dictFrmSz - dict of frame size
	#       pformat - pix format we are enumerating
	#
	def _enumFrameSz(self, dictFrmSz, pformat):
		if not self._fd:
                        return None
		#print 'creating', pformat
		index = 0
		while True:
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
			if (w, h) in dictFrmSz:
				print 'Duplicated frame size', w, 'x', h, '... ignored !!!!'
			else:
				if self._verbose > 2:
					print 'found', (w, h)
				dictFrmSz[(w, h)] = {}     #each is of key 'struct' and 'rate'
				dictFrmSz[(w, h)]['struct'] = efrmsz
				self._enumFrameIval(dictFrmSz[(w, h)], pformat, w, h)
			index += 1
		if 1==self._verbose:
			self.printFramerate(dictFrmSz, False)
		elif 2==self._verbose:
			self.printFramerate(dictFrmSz, True)
		return dictFrmSz


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
		choices=[0, 1, 2, 3])
	parser.add_argument('-d', type=int, action='store', default=0,
		dest='DEV_NR', help='it stands for /dev/video[DEV_NR]')
	parser.add_argument('-q', action='store_true', default=False,
		dest='query', help='show device information')
	args = parser.parse_args()
	dev = video('video'+str(args.DEV_NR), args.verbose)
        dev.querycap()
	dev.enumfmt()
	if args.query and not args.verbose:
		dev.printCap()
		dev.printFmt()
