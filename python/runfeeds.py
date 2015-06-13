#!/bin/env python2
import os
import sys
import signal
import time
import gobject

from camerafeed import CameraFeed

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


gobject.threads_init()
signal.signal(signal.SIGINT, handle_sigint)

for pipe, ip in CAMERA_FEEDS.items():
	feeds.append(CameraFeed(pipe, ip))

while os.path.exists(MIXER_PIPE):
	for feed in feeds:
		if not feed.is_running():
			feed.start()
	
	time.sleep(5)

teardown()
