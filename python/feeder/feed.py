#!/bin/env python2

import gi
gi.require_version('Gst', '1.0')
from gi.repository import  Gst

class Feed(object):

	def __init__(self, name):
		self._running = False
		self._thead = None
		self._pipeline = None
		self._name = name


	def is_running(self):
		return self._running


	def stop(self):
		if not self._running:
			return

		if self._pipeline <> None:
			print "[%s] pipeline stopped" % self._name
			self._pipeline.set_state(Gst.State.NULL)

		if self._thread <> None:
			print "[%s] waiting for thread to terminate" % self._name
			self._thread.join(2.0)
