# coding=Big5
import sys  
print sys.getdefaultencoding()  

s = '�A�n'
#turn big encoded string to utf-8 fails
#need to turn it to unicode first before encoding as utf-8
su = s.decode('big5').encode('utf-8')
print su

#both show Chinese correctly in docker/python 2.7
n = u'�A�n'
print n.encode('utf-8')





