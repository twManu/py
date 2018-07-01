#!/usr/bin/python
# coding: utf-8

"""
Python DBus example
"""
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
import gobject, dbus, dbus.service
from dbus.mainloop.glib import DBusGMainLoop


NAME = "blog.rock.sample.Hello"
DBUS_START="dbus-send --session --print-reply --dest="

def nameToPath(name):
	return "/"+name.replace(".", "/")

def usage():
	print "*** query service Hello ***"
	print DBUS_START+NAME,
	print nameToPath(NAME),
	print "org.freedesktop.DBus.Introspectable.Introspect"
	print
	print "*** invoke method Say ***"
	print DBUS_START+NAME,
	print nameToPath(NAME),
	print NAME+".Say string:\"Hello\""
	print
	print "*** trigger signal SignalSay ***"
	print DBUS_START+NAME,
	print "--type=signal",
	print nameToPath(NAME),
	print NAME+".SignalSay string:\"Hello\" uint32:5"
	print
	print "*** invoke method Stop ***"
	print DBUS_START+NAME,
	print nameToPath(NAME),
	print NAME+".Stop"
	print
	

class Hello(dbus.service.Object):
	"""
	Hello service. Inheriting from dbus.service.Object
	Service name: blog.rock.sample.Hello
	http://dbus.freedesktop.org/doc/dbus-python/api/dbus.service.Object-class.html
	API文件範例打錯了，此類別的名稱是首字大寫 dbus.service.Object ，不是 dbus.service.object
	"""
	name = NAME
	path = '/' + name.replace('.', '/')
	interface = name
	# In  :
	#     name - "blog.rock.sample.Hello" by default
	#
	def __init__(self, event_loop):
		"""
		http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html#inheriting-from-dbus-service-object
		教學文件打錯了，第三行的 path 應該是 object_path。同時，它漏了 BusName 。
		若按照教學文件的寫法，因為沒有指定 bus name ，故實際上是無用的。
		"""
		self.bus = dbus.SessionBus()
		self.event_loop = event_loop
		bus_name = dbus.service.BusName(Hello.name, bus=self.bus)
		dbus.service.Object.__init__(self, bus_name, Hello.path)
		self._init_notifier()

	def _init_notifier(self):
		notifications_service = 'org.freedesktop.Notifications'
		notifications_object = '/' + notifications_service.replace('.', '/')
		notifications_interface = notifications_service
		self.notifier = dbus.Interface(
			self.bus.get_object(notifications_service, notifications_object),
			notifications_interface)

	def _notify(self, title="", message="", icon="icon", timeout=0):
		self.notifier.Notify('Hello', 0, icon, title, message, [], {}, timeout*1000)


####
# Exporting method
# http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html#exporting-methods-with-dbus-service-method
# API: http://dbus.freedesktop.org/doc/dbus-python/api/dbus.service-module.html#method
# Signature of arguments: http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html#data-types
####

	@dbus.service.method(NAME, in_signature='s', out_signature='s')
	def Say(self, message):
		"""
		教學與範例文件打錯了，API 文件寫明 dbus.service.method 的第一個參數是位
		置參數，不是關鍵字參數，所以不能寫成 interface="..."
		"""
		self._notify(title="say", message=message, timeout=3)
		self.SignalSay(message, 3) # emmit signal
		return "I say " + message

	@dbus.service.method(NAME)
	def Stop(self):
		self.event_loop.quit()
####
# Exporting signal
# http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html#emitting-signals-with-dbus-service-signal
# API: http://dbus.freedesktop.org/doc/dbus-python/api/dbus.service-module.html#signal
####

	@dbus.service.signal(NAME, signature='su')
	def SignalSay(self, message, timeout):
		print message
		pass

class SignalRecipient:
	def __init__(self):
		"""
		DBus Signal 是廣播訊息。向 DBus 註冊訊號接收者時，通常會設定訊號過濾
		條件，否則所有訊號都會灌過來。
		一般指定 signal of service (by dbus_interface and signal_name) 為
		過濾條件。
		"""
		#self.dbus_object.connect_to_signal("SignalSay", self._ss,
		#                dbus_interface=Hello.interface, arg0="Hello")
		self.bus = dbus.SessionBus()
		self.bus.add_signal_receiver(self.handler,
				dbus_interface=Hello.interface,
				signal_name = "SignalSay")

	def handler(self, message, timeout):
		print "Signal recivied: %s, %d" % (message, timeout)


if __name__ == "__main__":
	usage()
	# You must do this before connecting to the bus.
	# http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html#setting-up-an-event-loop
	DBusGMainLoop(set_as_default=True)
	loop = gobject.MainLoop()

	service = Hello(loop)
	recipient = SignalRecipient()

	print "Working..."
	loop.run()  # startup event loop

