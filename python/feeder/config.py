#!/bin/env python2

CAMERA_FEEDS = {
	'/tmp/feed1' : '192.168.2.20',
	'/tmp/feed2' : '192.168.2.30',
	'/tmp/feed3' : '192.168.2.40',
}

MIXER_PIPE = '/tmp/mixer1'

MIXER_WIDTH = 1280
MIXER_HEIGHT = 720
MIXER_FRAMERATE = 25
SHM_SIZE = MIXER_WIDTH * MIXER_WIDTH * 4 * 26

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
OUTPUT_PORT = 6666



FEED_SOURCE = 'rtspsrc location=rtspt://%(ip)s ! rtph264depay ! h264parse ! avdec_h264'
MIXER_FORMAT = 'video/x-raw, format=BGRA,'\
				+ ' width=%(width)d, height=%(height)d, framerate=%(framerate)d/1, pixel-aspect-ratio=1/1'
SCALE = 'videorate ! videoscale ! videoconvert'
FEED_SINK = 'shmsink socket-path=%(feed_pipe)s shm-size=%(shm_size)d wait-for-connection=1 sync=true'

OUTPUT_SOURCE = 'shmsrc socket-path=%(mixer_pipe)s do-timestamp=true is-live=true'
SCREEN_OUTPUT = 'videoscale ! video/x-raw, format=BGRA, width=%(screen_width)d, height=%(screen_height)d !'\
				+ 'videoconvert ! timeoverlay ! ximagesink'
NETWORK_OUTPUT = 'videoconvert ! x264enc tune="zerolatency" ! video/x-h264, profile="high" ! mpegtsmux ! tcpserversink host=0.0.0.0 port=%(port)d'
