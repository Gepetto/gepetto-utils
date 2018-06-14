#!/bin/bash

ffmpeg \
    -i http://axis-ptz1/mjpg/video.mjpg \
    -t 10:00:00 \
    -c:v libx265 \
    axis-ptz1-$(date +'%Y-%m-%d-%A-%H:%M:%S').mp4
