#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import threading
import time
from datetime import datetime

class ClockController(object):

	TEXT_ID = 1

	def __init__(self, socket):
		self.snowmix_socket = socket

		self.update_thread = threading.Thread(target=self.update_clock)
		self.stopped = False
		self.update_thread.start()

	def update_clock(self):
		print "Starting update thread !"
		while not self.stopped:
			now = datetime.now()
			self.update_text(now.strftime("%H:%M:%S"))
			time.sleep(1.0)

		print "Stopping update thread !"


	def update_text(self, text):
		cmd = "text string %d %s\n" % (self.TEXT_ID,text)
		self.snowmix_socket.send(cmd)


	def stop(self):
		self.stopped = True
		self.update_thread.join(5.0)




