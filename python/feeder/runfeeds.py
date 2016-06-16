#!/bin/env python2
import os
import sys
import signal
import time

import gi
gi.require_version('Gst', '1.0')
from gi.repository import  Gst,GObject

from camerafeed import CameraFeed
from outputfeed import OutputFeed

from config import *

feeds = []

def teardown():
	print "[main] Stopping all remaining feeds"
	for feed in feeds:
		feed.stop()

def handle_sigint(signum, frame):
	print "[main] caught sigint"
	teardown()
	sys.exit(0)


GObject.threads_init()
Gst.init(None)
signal.signal(signal.SIGINT, handle_sigint)

for pipe, ip in CAMERA_FEEDS.items():
	feeds.append(CameraFeed(pipe, ip))

feeds.append(OutputFeed())

while os.path.exists(MIXER_PIPE):
	for feed in feeds:
		if not feed.is_running():
			feed.start()

	time.sleep(5)

teardown()
