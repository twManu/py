
CFLAGS=$(shell pkg-config --cflags python)
LDFLAGS=$(shell /usr/bin/python2.7-config --ldflags)
STATIC=
#STATIC=-static
#celsius: celsius.cpp
#	${CROSS_COMPILE}gcc -static ${CFLAGS} -o celsius celsius.cpp -lpython2.7 ${LDFLAGS}

celsius: celsius.cpp
	gcc ${STATIC} -I/usr/include/python2.7 -L/usr/lib -L/usr/lib/x86_64-linux-gnu -L/usr/lib/python2.7/config-x86_64-linux-gnu -L/usr/lib/python2.7/config/ -o celsius celsius.cpp -lpython2.7 -ldl -lm -lutil -pthread

clean:
	rm -f *.o
	rm -f celsius
