#!/bin/bash

gst-launch-1.0 -v tcpclientsrc host=mixer.htt port=6666 ! tsdemux ! h264parse ! omxh264dec ! eglglessink sync=false
