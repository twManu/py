from cVLCdtv import *

class cVLCatsc(cVLCdtv):
	def __init__(self):
		super(cVLCatsc, self).__init__(cVLCdtv.ATSC)


if __name__ == '__main__':
	obj = cVLCatsc()
	print(obj.getType())
	print(obj.getCmd())

