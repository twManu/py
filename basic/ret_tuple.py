def quadcube (x):
	return x**2, x**3
a, b = quadcube(3)
print(a)
print(b)

# lambda doesn't contain a return
# however it always contains an expression which is returned
g = lambda x: (x**2, x**3)   #() must be present
c, d = g(3)
print(c)
print(d)


def make_incrementor (n): return lambda x: x + n
f = make_incrementor(2)
g = make_incrementor(6)
print(f(42), g(42))
print(make_incrementor(22)(33))
 
