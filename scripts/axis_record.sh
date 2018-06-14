#!/bin/bash

ffmpeg -i http://axis-ptz1/mjpg/video.mjpg -c:v libx265 axis-ptz1-$(date +'%Y-%m-%d-%A-%H:%M:%S').mp4
