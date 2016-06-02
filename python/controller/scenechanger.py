#!/bin/env python2

class SceneChanger(object):

	def __init__(self, socket):
		self.cur_scene = 'Full'
		self.snowmix_socket = socket


	def switch_to(self, next_scene):
		if self.cur_scene != next_scene:
			cmd = "overlay finish Show%s\n" % (next_scene)
			self.snowmix_socket.send(cmd)
			self.cur_scene = next_scene
