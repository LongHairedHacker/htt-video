#!/bin/bash
# Deliver a webcam video as input feed 

if [ -z "$1" -o -z "$2" ]; then
	echo "Usage $0 <control pipe> <cam url>"
	exit
fi

CONTROL_PIPE="$1"
MIXERFORMAT='video/x-raw-rgb, bpp=(int)32, depth=32,  endianness=(int)4321, red_mask=(int)65280, green_mask=(int)16711680, blue_mask=(int)-16777216, width=(int)1024, height=(int)768, framerate=(fraction)24/1, pixel-aspect-ratio=(fraction)1/1, interlaced=(boolean)false'
SRC="souphttpsrc location=$2 ! jpegdec ! videorate"
SHMSIZE='shm-size=10000000'
SHMOPTION="wait-for-connection=0"
SHMSINK1="shmsink socket-path=$CONTROL_PIPE $SHMSIZE $SHMOPTION"
SCALE='ffmpegcolorspace ! videoscale ! ffmpegcolorspace'


while true ; do
    # Remove the named pipe if it exist
    rm -f $CONTROL_PIPE
    gst-launch-0.10 -v      \
        $SRC              ! \
        $SCALE            ! \
        $MIXERFORMAT      ! \
        $SHMSINK1
    sleep 2
done
exit
