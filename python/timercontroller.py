#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import threading
import time
from datetime import datetime

class TimerController(object):

	TEXT_ID = 2
	UMLAUTS = {
		'ä' : 'ae',
		'ü' : 'ue',
		'ö' : 'oe',
		'ß' : 'ss'
	}



	def __init__(self, socket):
		self.snowmix_socket = socket

		self.active_timer = None
		self.timers = {}

		self.update_thread = threading.Thread(target=self.update_timer)
		self.stopped = False
		self.update_thread.start()

	def start_timer(self, name):
		if not name in self.timers.keys():
			self.timers[name] = datetime.now()			

	def get_timers(self):
		return self.timers.keys()
	
	
	def hide_timer(self):
		self.active_timer = None
		self.hide_text()


	def set_active_timer(self, name):
		if name in self.timers.keys():
			self.active_timer = name


	def update_timer(self):
		print "Starting update thread !"
		while not self.stopped:
			if self.active_timer != None:
				delta = datetime.now() - self.timers[self.active_timer]
				hours, remainder = divmod(delta.total_seconds(), 3600)
				minutes, seconds = divmod(remainder, 60)
				self.update_text('%s: %d:%d:%d' % (self.active_timer, hours, minutes, seconds))
				pass
			time.sleep(1.0)
		
		print "Stopping update thread !"
	
	
	def update_text(self, text):
		for umlaut, replacement in self.UMLAUTS.items():
			text = text.replace(umlaut, replacement)			

		cmd = "text string %d %s\n" % (self.TEXT_ID,text)
		self.snowmix_socket.send(cmd)

	
	def hide_text(self):
		cmd = "text string %d\n" % self.TEXT_ID
		self.snowmix_socket.send(cmd)


	def stop(self):
		self.stopped = True
		self.update_thread.join(5.0)



			
