#!/bin/env python2
import pygst
pygst.require('0.10')
import gst

pipeline = gst.Pipeline('pipeline')

file_src = gst.element_factory_make('filesrc', 'source');
file_src.set_property('location', '../videos/tears_of_steel_720p.mkv')

matroskademux = gst.element_factory_make('matroskademux')
h264parse = gst.element_factory_make('h264parse')
ffdec_h264 = gst.element_factory_make('ffdec_h264')

colorspace1 = gst.element_factory_make('ffmpegcolorspace')
videoscale = gst.element_factory_make('videoscale')
colorspace2 = gst.element_factory_make('ffmpegcolorspace')

caps = gst.Caps('video/x-raw-rgb, bpp=(int)32, endianness=(int)4321, format=(fourcc)BGRA, red_mask=(int)65280, green_mask=(int)16711680, blue_mask=(int)-16777216, width=(int)1280, height=(int)720, framerate=(fraction)24/1, pixel-aspect-ratio=(fraction)1/1, interlaced=(boolean)false')
caps_filter = gst.element_factory_make('capsfilter')
caps_filter.set_property('caps', caps);

ximagesink = gst.element_factory_make('ximagesink')

pipeline.add(file_src, matroskademux, h264parse, ffdec_h264, colorspace1, videoscale, colorspace2, caps_filter, ximagesink)
gst.element_link_many(file_src, matroskademux)
gst.element_link_many(h264parse, ffdec_h264, colorspace1, videoscale, colorspace2, caps_filter, ximagesink)

def on_new_demux_pad(element):
	matroskademux.link(h264parse)
	pipeline.set_state(gst.STATE_PLAYING)

matroskademux.connect('no-more-pads', on_new_demux_pad)

pipeline.set_state(gst.STATE_PAUSED)


bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
    gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
print msg

pipeline.set_state(gst.STATE_NULL)
