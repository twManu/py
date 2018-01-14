c-py
====

Calling python classes from within C++ code &amp; Python source designed to demonstrate the use of python embedding

prepare:
	$ export PYTHONPATH=${PYTHONPATH}:./

success call:
	$ ./call_function py_thread ThreadFunc
	$ ./call_function py_thread createThread
	$ ./call_function py_function multiply
	$ ./call_function py_function multiply1 2 3
	$ ./call_class py_thread MyThread run
	$ ./call_class py_class Multiply multiply
	$ ./call_class celsius c2 farenheit
	$ ./call_thread py_thread MyThread run
	# a b look dummy
	$ ./call_thread_2 py_thread MyThread a b
