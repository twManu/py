#!/usr/bin/python
# to be run under tisdk/build

import os, sys, glob

CLN_DIRS=(
	  'arago-tmp-external-linaro-toolchain/work/am57xx_evm-linux-gnueabi'
	, 'arago-tmp-external-linaro-toolchain/work/cortexa15hf-vfp-neon-linux-gnueabi'
	, 'arago-tmp-external-linaro-toolchain/work/all-linux'
)

for thisDir in CLN_DIRS:
	print 'Processing '+thisDir
	for ff in glob.glob(thisDir+'/*'):
		baseFF=os.path.basename(ff)
		print '  Cleaning '+baseFF
		os.system('MACHINE=am57xx-evm bitbake -f -c clean '+baseFF)
#looks fail		os.system('MACHINE=am57xx-evm bitbake -f -c cleanall '+baseFF)


os.system('MACHINE=am57xx-evm bitbake -f -c cleanall arago-core-tisdk-image')
