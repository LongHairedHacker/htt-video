#!/bin/env python2

class SceneChanger(object):

	def __init__(self, socket):
		self.cur_scene = 1
		self.snowmix_socket = socket


	def switch_to(self, next_scene):
		if self.cur_scene != next_scene:
			cmd = "Swap%d%d\n" % (self.cur_scene, next_scene)
			self.snowmix_socket.send(cmd)
			self.cur_scene = next_scene
