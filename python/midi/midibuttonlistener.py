#!/bin/env python2

import rtmidi


class MidiButtonListener(object):
	
	def __init__(self):
		self.midi_in = rtmidi.MidiIn()
		self.listeners = {}


	def _hex_message(self, message):
		return map(lambda x: hex(x), message)


	def _get_listeners(self, type, data1, data2):
			if not type in self.listeners.keys():
				return []

			if not data1 in self.listeners[type].keys():
				return []

			if not data2 in self.listeners[type][data1].keys():
				return []

			return self.listeners[type][data1][data2]

	def _enumarate_listeners(self, message_type, message_data1, message_data2):
		result = []
		for type in [None, message_type]:
			for data1 in [None, message_data1]:
				for data2 in [None, message_data2]:
					result += self._get_listeners(type,data1,data2)

		return result


	def add_listener(self, listener, type = None, data1 = None, data2 = None):

			if not type in self.listeners.keys():
				self.listeners[type] = {}

			if not data1 in self.listeners[type].keys():
				self.listeners[type][data1] = {}

			if not data2 in self.listeners[type][data1].keys():
				self.listeners[type][data1][data2] = []

			self.listeners[type][data1][data2].append(listener)


	def remove_listener(self, listener, type = None, data1 = None, data2 = None):
			if not type in self.listeners.keys():
				raise ValueError("No listener registered for %s" % hex(type))

			if not data1 in self.listeners[type].keys():
				raise ValueError("No listener registered for %s %s" % (hex(type), hex(data1)))

			if not data2 in self.listeners[type][data1].keys():
				raise ValueError("No listener registered for %s %s" % (hex(type), hex(data1), hex(data2)))

			self.listeners[type][data1][data2].remove(listener)


	def open(self, name):
		input_port = None
		for port_number in range(self.midi_in.get_port_count()):
			port_name = self.midi_in.get_port_name(port_number)
			print "Found port %d: %s" % (port_number, port_name)
			if port_name.startswith(name):
				input_port = port_number

		if not input_port:
			print "No matching midi device found"
			raise ValueError("No matching midi device found")

		self.midi_in.open_port(input_port)


	def process_messages(self):
		while(True):
			message = self.midi_in.get_message()
			if message:
				print "Print new message: %s " % self._hex_message(message[0])
				type, data1, data2 = message[0]
				for listener in self._enumarate_listeners(type, data1, data2):
					listener(type,data1,data2)


	def close(self):
		self.midi_in.close_port()


		