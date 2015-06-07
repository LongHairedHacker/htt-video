#!/bin/env python2
import pygst
pygst.require('0.10')
import gst

width = 1280
height = 720
pipe = "/tmp/feed1"
shm_size = 10000000


MIXERFORMAT = 'video/x-raw-rgb, bpp=(int)32, endianness=(int)4321, format=(fourcc)BGRA, red_mask=(int)65280, green_mask=(int)16711680, blue_mask=(int)-16777216, width=(int)%d, height=(int)%d, framerate=(fraction)60/1, pixel-aspect-ratio=(fraction)1/1, interlaced=(boolean)false' % (width, height)

SRC = 'rtspsrc location=rtsp://192.168.1.100 ! rtph264depay ! h264parse ! ffdec_h264'
SCALE = 'ffmpegcolorspace ! videorate ! videoscale ! ffmpegcolorspace'
#SINK = 'shmsink socket-path=%s shm-size=%d wait-for-connection=0' % (pipe, shm_size)
SINK = "ximagesink"

pipeline = gst.parse_launch('%s ! %s ! %s ! %s' % (SRC, SCALE, MIXERFORMAT, SINK))

pipeline.set_state(gst.STATE_PLAYING)

bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
    gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
print msg

pipeline.set_state(gst.STATE_NULL)
