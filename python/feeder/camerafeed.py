#!/bin/env python2
import os
import threading
from time import sleep

import gi
gi.require_version('Gst', '1.0')
from gi.repository import  Gst

from feed import Feed

from config import *

class CameraFeed(Feed):
	def __init__(self, feed_pipe, camera_ip):
		super(CameraFeed, self).__init__(feed_pipe)

		self._feed_pipe = feed_pipe
		self._camera_ip = camera_ip

	def start(self):
		if self.is_running():
			return

		if not os.path.exists(MIXER_PIPE):
			print '[%s] not starting because mixer is not running (pipe is missing)' % self._name
			return

		if os.path.exists(self._feed_pipe):
			print '[%s] not starting because feed pipe already exists' % self._name
			return

		print '[%s] is starting' % self._name
		self._running = True
		self._thread = threading.Thread(target=self._run)
		self._thread.start()


	def _run(self):
		src = FEED_SOURCE % {'ip': self._camera_ip}
		mixer_format = MIXER_FORMAT % {'width' : MIXER_WIDTH, 'height' : MIXER_HEIGHT, 'framerate' : MIXER_FRAMERATE}
		sink = FEED_SINK % {'feed_pipe' : self._feed_pipe, 'shm_size' : SHM_SIZE}

		print '%s ! %s ! %s ! %s' % (src, SCALE, mixer_format, sink)

		self._pipeline = Gst.parse_launch('%s ! %s ! %s ! %s' % (src, SCALE, mixer_format, sink))

		self._pipeline.set_state(Gst.State.PLAYING)
		print "[%s] is playing" % self._name

		bus = self._pipeline.get_bus()
		msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)
		print "[%s] %s" % (self._name, msg.parse_error()[1])

		self._pipeline.set_state(Gst.State.NULL)

		self._running = False

		print "[%s] has stopped" % self._name
