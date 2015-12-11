# coding=Big5
import sys  
print sys.getdefaultencoding()  

s = '你好'
#turn big encoded string to utf-8 fails
#need to turn it to unicode first before encoding as utf-8
su = s.decode('big5').encode('utf-8')
print su

#both show Chinese correctly in docker/python 2.7
n = u'你好'
print n.encode('utf-8')





