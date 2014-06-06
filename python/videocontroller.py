#!/usr/bin/env python

import sys
from gi.repository import Gtk

from scenechange import SceneChange

class VideoController:
	def __init__(self):
		
		self.scenechange = SceneChange()

		self.gladefile = "videocontroler.ui"  
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladefile)

		self.main_window = self.builder.get_object("MainWindow")
		self.max_cam1_button = self.builder.get_object("MaxCam1Button")
		self.max_cam2_button = self.builder.get_object("MaxCam2Button")
		self.max_cam3_button = self.builder.get_object("MaxCam3Button")

		self.messagebox = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "I'm afaraid I can't let you do that dave.")

		self.builder.connect_signals(self)
		self.main_window.show_all()



	def MaxCam1ButtonToggled(self, widget):
		if self.max_cam1_button.get_active():
			self.max_cam2_button.set_active(False)
			self.max_cam3_button.set_active(False)
			self.scenechange.switch_to(1)
		else:
			if not self.max_cam2_button.get_active() and not self.max_cam3_button.get_active():
				self.max_cam1_button.set_active(True)
	

	def MaxCam2ButtonToggled(self, widget):
		if self.max_cam2_button.get_active():
			self.max_cam1_button.set_active(False)
			self.max_cam3_button.set_active(False)
			self.scenechange.switch_to(2)
		else:
			if not self.max_cam1_button.get_active() and not self.max_cam3_button.get_active():
				self.max_cam2_button.set_active(True)


	def MaxCam3ButtonToggled(self, widget):
		if self.max_cam3_button.get_active():
			self.max_cam1_button.set_active(False)
			self.max_cam2_button.set_active(False)
			self.scenechange.switch_to(3)
		else:
			if not self.max_cam1_button.get_active() and not self.max_cam2_button.get_active():
				self.max_cam3_button.set_active(True)




	def MainWindowDelete(self, widget, event):
		if self.messagebox.run() == Gtk.ResponseType.OK:
			Gtk.main_quit()
		
		self.messagebox.hide()
		return True

videocontroller = VideoController()
Gtk.main()
