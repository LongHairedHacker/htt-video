MIXERCAPS='video/x-raw-rgb, bpp=(int)32, depth=32, endianness=(int)4321, red_mask=(int)65280, green_mask=(int)16711680, blue_mask=(int)-16777216, width=(int)1024, height=(int)768, framerate=(fraction)24/1, pixel-aspect-ratio=(fraction)1/1, interlaced=(boolean)false'


gst-launch-0.10 -v souphttpsrc location=http://schumb:frederik@192.168.11.10/videostream.cgi?rate=0 ! jpegdec  ! ffmpegcolorspace ! videoscale ! ffmpegcolorspace ! $MIXERCAPS ! ximagesink
