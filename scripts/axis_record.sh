#!/bin/bash

# You Only Record Once
pgrep ffmpeg > /dev/null && echo "ffmpeg is already running" && exit 1

# Remove mp4 files that have not been modified for one week
find . -name \*.mp4 -mtime +7 -delete

ffmpeg \
    -i http://axis-ptz1/mjpg/video.mjpg \
    -t 10:00:00 \
    -c:v libx265 \
    bauzil_axis-ptz1_$(date +'%Y-%m-%d_%A_%H%M%S').mp4
