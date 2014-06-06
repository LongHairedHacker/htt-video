#!/bin/env python2
import socket

class SceneChange(object):

	def __init__(self):
		self.cur_scene = 1
		self.snowmix_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.snowmix_socket.connect(("localhost", 9999))


	def switch_to(self, next_scene):
		if self.cur_scene != next_scene:
			cmd = "Swap%d%d\n" % (self.cur_scene, next_scene)
			self.snowmix_socket.send(cmd)
			self.cur_scene = next_scene
