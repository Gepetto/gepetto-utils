#!/bin/bash -eu

source /dist

if [ "$DIST" = "archlinux" ]
then echo /opt/openrobots/lib/python2.7/site-packages/ > /usr/lib/python2.7/site-packages/robotpkg.pth
fi

if [ "$DIST" != "20.04" ]
then
    echo python 2
    grep "Boost_PYTHON_LIBRARY " /src/eigenpy/build2/config.log
fi
echo python 3
grep "Boost_PYTHON_LIBRARY " /src/eigenpy/build3/config.log
