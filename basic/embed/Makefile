
STATIC=
#STATIC=-static
CFLAGS=${STATIC} -I/usr/include/python2.7 -L/usr/lib -L/usr/lib/x86_64-linux-gnu -L/usr/lib/python2.7/config-x86_64-linux-gnu -L/usr/lib/python2.7/config
LDFLAGS=-lpython2.7 -ldl -lm -lutil -pthread
TARGET=call_class call_function call_thread call_thread_2
#celsius: celsius.cpp
#	${CROSS_COMPILE}gcc -static ${CFLAGS} -o celsius celsius.cpp -lpython2.7 ${LDFLAGS}
.PHONY: all
all: ${TARGET}
call_class: call_class.c
	gcc ${CFLAGS} -o $@ $< ${LDFLAGS}
call_function: call_function.c
	gcc ${CFLAGS} -o $@ $< ${LDFLAGS}
call_thread: call_thread.c
	gcc ${CFLAGS} -o $@ $< ${LDFLAGS}
call_thread_2: call_thread_2.c
	gcc ${CFLAGS} -o $@ $< ${LDFLAGS}

clean:
	rm -f *.o
	rm -f ${TARGET}
