#!/bin/bash -eux

# Install cmake, ninja and wheel
PY39_BIN=/opt/python/cp39-cp39/bin
$PY39_BIN/pip install cmake ninja wheel
ln -s $PY39_BIN/cmake /usr/bin/
ln -s $PY39_BIN/ninja /usr/bin/
ln -s $PY39_BIN/wheel /usr/bin/

# Setup python 2.7
yum -y install python-pip
PY27_BIN=/opt/python/cp27-cp27mu/bin
mkdir -p $PY27_BIN
ln -s /usr/bin/python $PY27_BIN/
ln -s /usr/bin/pip $PY27_BIN/

# Upgrade pip and install scikit-build
for PYBIN in /opt/python/*/bin; do
    if "$PYBIN"/pip --version | grep -q 2.7
    then "$PYBIN"/pip install --upgrade "pip<21"
    else "$PYBIN"/pip install --upgrade pip
    fi
    "$PYBIN"/pip install --user scikit-build numpy
done
