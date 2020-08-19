#!/bin/bash -eu

source /dist

if [ "$DIST" != "20.04" ]
then python2 /run.py
fi
python3 /run.py
