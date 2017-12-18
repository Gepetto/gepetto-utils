# Scripts for Gepetto

## `release.sh`

`./release.sh <tag> [<package name>]`

Creates a signed tag named `v<tag>` and push it.
Also creates `<package name>-<tag>.tar.gz{,.sig}` including submodules.

## `video.py`

```
usage: video.py [-h] [--image IMAGE] [-ss START_TIME] [-to END_TIME] [-n N]
                [-fs FS] [--no-magic] [-c]
                rush author title

Append a title slide to a video. Optionnaly cut it and crop it.

positional arguments:
  rush                  filename of the rush
  author                speaker's name
  title                 talk's title

optional arguments:
  -h, --help            show this help message and exit
  --image IMAGE         title image
  -ss START_TIME, --start-time START_TIME
                        start of the video
  -to END_TIME, --end-time END_TIME
                        end of the video
  -n N                  number of the video in a playlist (0 for no playlist)
  -fs FS                font size
  --no-magic
  -c, --crop            Crop the speaker only from the video
```
