# Scripts for Gepetto

## `doc.py` & `doc.sh`

Gets the projects / namespaces / branches to process from the [Gepetto Dashboard](http://rainboard.laas.fr)
(activate `keep_doc` on the branches you need)
Run them in this order in a cron job to put the last generated doxygen HTML from gepgitlab on
`/net/cetus/data/gepetto/Doc`.

## `release.sh`

`./release.sh <tag> [<package name>]`

Creates a signed tag named `v<tag>` and push it.
Also creates `<package name>-<tag>.tar.gz{,.sig}` including submodules.

Can be usefull if you don't have the JRL cmake submodule, otherwise just use `make release VERSION=x.y.z && make dist`

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

## `parse_muscod_logs.py`

```
usage: parse_muscod_logs.py [-h] [-v] filename

Parse muscod's logs to get NDIS, the number of iterations & total computation
time

positional arguments:
  filename

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
```

## `axis_play.sh` & `axis_record.sh`

The first allows to check that the camera is configured correctly.
If you are not satisfied, you have to use the [web interface](http://axis-ptz1).

The second records the current view. It is meant to be run in `eur0c:/local/axis`

## `searchLib.sh`

```
usage: searchLib.sh my_lib version_to_avoid
```
This script searches all the .so files in the current directory.
The first arg is a string contained in the dependencies of the library you are looking for.
The second arg is a string contained in the dependencies that you want to reject. 
The script will display the names of the .so files which meet these criteria.

