#!/bin/sh

gst-launch-1.0 -vvv v4l2src device=/dev/video0 do-timestamp=true !\
	image/jpeg, width=1920, height=1080, framerate=30/1 !\
	jpegparse ! jpegdec !\
	videoconvert ! xvimagesink sync=false
