#!/bin/env python2
import os
import threading
from time import sleep

import pygst
pygst.require('0.10')
import gst

from config import *

WIDTH = 1280
HEIGHT = 720
FRAMERATE = 25
SHM_SIZE = 10000000

class CameraFeed(object):
	def __init__(self, feed_pipe, camera_ip):
		self._feed_pipe = feed_pipe
		self._camera_ip = camera_ip
		self._running = False
		self._pipeline = None
		self._thead = None

	def start(self):
		if self._running:
			return

		if not os.path.exists(MIXER_PIPE):
			print '[%s] not starting because mixer is not running (pipe is missing)' % self._feed_pipe
			return

		if os.path.exists(self._feed_pipe):
			print '[%s] not starting because feed pipe already exists' % self._feed_pipe
			return
		
		print '[%s] is starting' % self._feed_pipe
		self._running = True
		self._thread = threading.Thread(target=self._run)		
		self._thread.start()


	def is_running(self):
		return self._running

	
	def stop(self):

		if not self._running:
			return
		
		if self._pipeline <> None:
			print "[%s] pipeline stopped" % self._feed_pipe
			self._pipeline.set_state(gst.STATE_NULL)
		
		if self._thread <> None:
			print "[%s] waiting for thread to terminate" % self._feed_pipe
			self._thread.join(2.0)


	def _run(self):
		src = FEED_SOURCE % {'ip': self._camera_ip}
		mixer_format = MIXER_FORMAT % {'width' : MIXER_WIDTH, 'height' : MIXER_HEIGHT, 'framerate' : MIXER_FRAMERATE}
		sink = FEED_SINK % {'feed_pipe' : self._feed_pipe, 'shm_size' : SHM_SIZE}

		self._pipeline = gst.parse_launch('%s ! %s ! %s ! %s' % (src, SCALE, mixer_format, sink))

		self._pipeline.set_state(gst.STATE_PLAYING)
		print "[%s] is playing" % self._feed_pipe

		bus = self._pipeline.get_bus()
		msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE, gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
		print "[%s] %s" % (self._feed_pipe, msg.parse_error()[1])

		self._pipeline.set_state(gst.STATE_NULL)

		self._running = False
		
		print "[%s] has stopped" % self._feed_pipe
