#!/bin/env python2
import pygst
pygst.require('0.10')
import gst

MIXER_IP = 'localhost'
MIXER_PORT = 9999

class CameraFeed(object):

	def __init__(self, pipe, cam_ip):
		self.pipe = pipe
		self.cam_ip = cam_ip

	def _run(self):
		snowmix_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		snowmix_socket.connect((ip, 9999))


