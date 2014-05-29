MIXERCAPS='video/x-raw-rgb, width=(int)1024, height=(int)768'


gst-launch-0.10 -v souphttpsrc location=http://gstreamer:GlytEnru@$1/videostream.cgi?rate=0 ! jpegdec  ! ffmpegcolorspace ! videoscale ! ffmpegcolorspace ! $MIXERCAPS ! ximagesink
