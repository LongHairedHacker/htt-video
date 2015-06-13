#!/bin/env python2

CAMERA_FEEDS = {
	'/tmp/feed1' : '192.168.1.100', 
	'/tmp/feed2' : '192.168.1.101', 
	'/tmp/feed3' : '192.168.1.102',
}

MIXER_PIPE = '/tmp/mixer1'

MIXER_WIDTH = 1280
MIXER_HEIGHT = 720
MIXER_FRAMERATE = 25
SHM_SIZE = 10000000

FEED_SOURCE = 'rtspsrc location=rtsp://%(ip)s ! rtph264depay ! h264parse ! ffdec_h264'
MIXER_FORMAT = 'video/x-raw-rgb, bpp=(int)32, endianness=(int)4321, format=(fourcc)BGRA,'\
				+ ' red_mask=(int)65280, green_mask=(int)16711680, blue_mask=(int)-16777216,'\
				+ ' width=(int)%(width)d, height=(int)%(height)d, framerate=(fraction)%(framerate)d/1,'\
				+ 'pixel-aspect-ratio=(fraction)1/1, interlaced=(boolean)false'
SCALE = 'ffmpegcolorspace ! videorate ! videoscale ! ffmpegcolorspace'
FEED_SINK = 'shmsink socket-path=%(feed_pipe)s shm-size=%(shm_size)d wait-for-connection=0'

