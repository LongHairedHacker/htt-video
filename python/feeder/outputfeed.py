#!/bin/env python2
import os
import threading
from time import sleep

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

from feed import Feed

from config import *


class OutputFeed(Feed):
	def __init__(self):
		super(OutputFeed, self).__init__(MIXER_PIPE)


	def start(self):
		if self.is_running():
			return

		if not os.path.exists(MIXER_PIPE):
			print '[%s] not starting because mixer is not running (pipe is missing)' % self._name
			return


		print '[%s] is starting' % self._name
		self._running = True
		self._thread = threading.Thread(target=self._run)
		self._thread.start()


	def _run(self):
		src = OUTPUT_SOURCE % {'mixer_pipe' : MIXER_PIPE}
		mixer_format = MIXER_FORMAT % {'width' : MIXER_WIDTH, 'height' : MIXER_HEIGHT, 'framerate' : MIXER_FRAMERATE}
		screen_output = SCREEN_OUTPUT % {'screen_width' : SCREEN_WIDTH, 'screen_height' : SCREEN_HEIGHT}
		network_output = NETWORK_OUTPUT % {'port' : OUTPUT_PORT}

		pipeline = '%s ! %s ! queue leaky=2 ! tee name=split ! queue leaky=2 ! %s split. ! queue leaky=2 ! %s' % (src,
																									mixer_format,
																									screen_output,
																									network_output)
		print pipeline
		self._pipeline = Gst.parse_launch(pipeline)



		self._pipeline.set_state(Gst.State.PLAYING)
		print "[%s] is playing" % self._name

		bus = self._pipeline.get_bus()
		msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)
		print "[%s] %s" % (self._name, msg.parse_error()[1])

		self._pipeline.set_state(Gst.State.NULL)

		self._running = False

		print "[%s] has stopped" % self._name
