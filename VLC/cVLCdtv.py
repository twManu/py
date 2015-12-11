from cVLCbase import *

class cVLCdtv(cVLCbase):
	DVB = 1
	ATSC = 2
	CQAM = 3

	def __init__(self, subtype = DVB):
		super(cVLCdtv, self).__init__(cVLCbase.DTV+subtype)

	#return readable string of type of command
	def getType(self):
		if self._type > cVLCbase.DTV or self._type < cVLCbase.DTV+10:
			subtype = self._type - cVLCbase.DTV
			if self.DVB == subtype:
				return "DVB"
			elif self.ATSC == subtype:
				return "ATSC"
			elif self.CQAM == subtype:
				return "clearQAM"
		return super(cVLCdtv, self).getType(self)

if __name__ == '__main__':
	obj = cVLCdtv()
	print(obj.getType())
	print(obj.getCmd())

