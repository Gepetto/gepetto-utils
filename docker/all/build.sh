#!/bin/bash -eux

export DIST=$1
export PYTHON=$2

if [ "$DIST" = "archlinux" ] && [ "$PYTHON" = "python2" ]
then pacman -Sy --noconfirm python2-numpy
fi
git clone --recursive --depth 1 --branch topic/multipy2 https://github.com/nim65s/eigenpy.git
mkdir eigenpy/build
cd eigenpy/build || exit 1
cmake -DPYTHON_EXECUTABLE="/usr/bin/$PYTHON" ..
