#!/bin/bash

MIXERFORMAT='video/x-raw-rgb, bpp=(int)32, endianness=(int)4321, format=(fourcc)BGRA, red_mask=(int)65280, green_mask=(int)16711680, blue_mask=(int)-16777216, width=(int)1280, height=(int)720, framerate=(fraction)24/1, pixel-aspect-ratio=(fraction)1/1, interlaced=(boolean)false'

SRC='videotestsrc pattern=snow horizontal-speed=25' 

SCALE='ffmpegcolorspace ! videoscale ! ffmpegcolorspace'

NETWORK='queue ! timeoverlay ! ffmpegcolorspace ! x264enc tune="zerolatency" ! mpegtsmux ! tcpserversink host=0.0.0.0 port=6666'

gst-launch-0.10 -v    \
	$SRC            !\
	$SCALE 			!\
	$MIXERFORMAT	!\
	$NETWORK
    
