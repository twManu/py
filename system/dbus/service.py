#!/usr/bin/env python
# Copyright (C) 2004-2006 Red Hat Inc. <http://www.redhat.com/>
# Copyright (C) 2005-2007 Collabora Ltd. <http://www.collabora.co.uk/>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# sudo apt-get install -y python-dbus python-dbus-dev python-gobject
#
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

class DemoException(dbus.DBusException):
	_dbus_error_name = 'com.example.DemoException'

class SomeObject(dbus.service.Object):

	@dbus.service.method("com.example.SampleInterface", in_signature='s', out_signature='as')
	def HelloWorld(self, hello_message):
		print (str(hello_message))
		return ["Hello", " from example-service.py", "with unique name",
			session_bus.get_unique_name()]

	@dbus.service.method("com.example.SampleInterface", in_signature='', out_signature='')
	def Exit(self):
		mainloop.quit()


if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	session_bus = dbus.SessionBus()
	name = dbus.service.BusName("com.example.SampleService", session_bus)
	object = SomeObject(session_bus, '/SomeObject')
	mainloop = gobject.MainLoop()
	print "Running example service."
	mainloop.run()

