def path_chip_map(path):
	def deco_map(func):
		def func_wrapper(*args, **kwargs):
			p1, p2 = func(*args, **kwargs)
			if p1 is None:
				if p2 is None:
					return None, None
				else:
					return None, path+'/gpio'+str(p2)
			return path+'/gpiochip'+str(p1),\
		       	       path+'/gpio'+str(p2)
		return func_wrapper
	return deco_map

@path_chip_map('/sys/class/gpio')
def am57_gpio(chip, pin):
	"""chip=1-8, pin=0-31 """
	if chip<=0 or chip>8:
		return None, None
	chip = chip - 1
	if pin<0 or pin>=32:
		return None, None
	return chip, 32*chip+pin

if __name__ == '__main__':
	print am57_gpio(1, 22)
