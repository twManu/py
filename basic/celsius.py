#!/usr/bin/python
#import celsius
#obj = celsius.celsius(100)
#print obj.farenheit()

class celsius:
	def __init__(self, degrees):
		self.degrees = degrees
	def farenheit(self):
		return ((self.degrees*9.0)/5.0)+32.0

class c2(celsius):
	def __init__(self):
		super(c2, self).__init__(100)

# main
if __name__ == '__main__':
	obj = celsius(100)
	print obj.farenheit()
	obj2 = c2()
	print obj2.farenheit()
