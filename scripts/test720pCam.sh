#!/bin/bash


MIXERFORMAT='video/x-raw-rgb, bpp=(int)32, endianness=(int)4321, format=(fourcc)BGRA, red_mask=(int)65280, green_mask=(int)16711680, blue_mask=(int)-16777216, width=(int)1280, height=(int)720, framerate=(fraction)60/1, pixel-aspect-ratio=(fraction)1/1, interlaced=(boolean)false'

SRC="rtspsrc location=rtsp://192.168.1.100 ! rtph264depay ! h264parse ! ffdec_h264"
SCALE='ffmpegcolorspace ! videorate ! videoscale ! ffmpegcolorspace'

SINK='ximagesink'
SINK='shmsink socket-path=/tmp/feed1 shm-size=10000 wait-for-connection=0'



gst-launch-0.10 -v   \
	$SRC            !\
	$SCALE 			!\
	$MIXERFORMAT	!\
    $SINK

