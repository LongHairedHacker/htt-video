#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import socket
from gi.repository import Gtk, GObject

from scenechanger import SceneChanger
from clockcontroller import ClockController

class VideoController(object):
	def __init__(self, ip):

		self.snowmix_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.snowmix_socket.connect((ip, 9999))

		self.scenechanger = SceneChanger(self.snowmix_socket)
		self.clockcontroller = ClockController(self.snowmix_socket)

		self.gladefile = "videocontroller.ui"
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladefile)

		self.main_window = self.builder.get_object("MainWindow")
		self.max_cam1_button = self.builder.get_object("MaxCam1Button")
		self.max_cam2_button = self.builder.get_object("MaxCam2Button")
		self.max_cam3_button = self.builder.get_object("MaxCam3Button")
		self.show_all_button = self.builder.get_object("ShowAllButton")

		self.messagebox = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "I'm afaraid I can't let you do that dave.")

		self.builder.connect_signals(self)
		self.main_window.show_all()


	def MaxCam1ButtonToggled(self, widget):
		if self.max_cam1_button.get_active():
			self.max_cam2_button.set_active(False)
			self.max_cam3_button.set_active(False)
			self.show_all_button.set_active(False)
			self.scenechanger.switch_to('Full1')
		else:
			if not self.max_cam2_button.get_active() and not self.max_cam3_button.get_active() and not self.show_all_button.get_active():
				self.max_cam1_button.set_active(True)

	def MaxCam2ButtonToggled(self, widget):
		if self.max_cam2_button.get_active():
			self.max_cam1_button.set_active(False)
			self.max_cam3_button.set_active(False)
			self.show_all_button.set_active(False)
			self.scenechanger.switch_to('Full2')
		else:
			if not self.max_cam1_button.get_active() and not self.max_cam3_button.get_active() and not self.show_all_button.get_active():
				self.max_cam2_button.set_active(True)


	def MaxCam3ButtonToggled(self, widget):
		if self.max_cam3_button.get_active():
			self.max_cam1_button.set_active(False)
			self.max_cam2_button.set_active(False)
			self.show_all_button.set_active(False)
			self.scenechanger.switch_to('Full3')
		else:
			if not self.max_cam1_button.get_active() and not self.max_cam2_button.get_active() and not self.show_all_button.get_active():
				self.max_cam3_button.set_active(True)

	def ShowAllButtonToggled(self, widget):
		if self.show_all_button.get_active():
			self.max_cam1_button.set_active(False)
			self.max_cam2_button.set_active(False)
			self.max_cam3_button.set_active(False)
			self.scenechanger.switch_to('All')
		else:
			if not self.max_cam1_button.get_active() and not self.max_cam2_button.get_active() and not self.max_cam3_button.get_active():
				self.show_all_button.set_active(True)


	def MainWindowDelete(self, widget, event):
		if self.messagebox.run() == Gtk.ResponseType.OK:
			self.clockcontroller.stop()
			Gtk.main_quit()

		self.messagebox.hide()
		return True

if len(sys.argv) != 2:
	print "Usage %s <remote ip>" % sys.argv[0]
	sys.exit(-1)

videocontroller = VideoController(sys.argv[1])
GObject.threads_init()
Gtk.main()
