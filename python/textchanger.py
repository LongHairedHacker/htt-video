#!/bin/env python2
# -*- coding: utf-8 -*-

class TextChanger(object):

	TEXT_ID = 1
	UMLAUTS = {
		'ä' : 'ae',
		'ü' : 'ue',
		'ö' : 'oe',
		'ß' : 'ss'
	}

	def __init__(self, socket):
		self.snowmix_socket = socket
		

	def set_text(self, text):
		for umlaut, replacement in self.UMLAUTS.items():
			text = text.replace(umlaut, replacement)			

		cmd = "text string %d %s\n" % (self.TEXT_ID,text)
		self.snowmix_socket.send(cmd)

	def hide_text(self):
		cmd = "text string %d\n" % self.TEXT_ID
		self.snowmix_socket.send(cmd)

		
