#!/usr/bin/python

import datetime, time

t1 = datetime.datetime.now()
for i in range(10):
	time.sleep(1)
	dt = datetime.datetime.now() - t1
	seconds = dt.total_seconds()
	print 'delta sec:', seconds

