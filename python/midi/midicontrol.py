#!/bin/env python2

import sys

from midibuttonlistener import MidiButtonListener

from scenechange import SceneChange


INPUT_NAME = "USB Midi"

buttonlistener = MidiButtonListener()

buttonlistener.open(INPUT_NAME)

sc = SceneChange()

buttonlistener.add_listener(sc.bind_switch(1),0xb9,0x08)
buttonlistener.add_listener(sc.bind_switch(2),0xb9,0x0a)
buttonlistener.add_listener(sc.bind_switch(3),0xb9,0x0b)

buttonlistener.process_messages()