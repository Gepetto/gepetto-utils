#!/bin/bash -eux

# Don't build wheels for python 3.9
rm -rf /opt/python/cp39-cp39

# Install cmake, ninja and wheel
PY38_BIN=/opt/python/cp38-cp38/bin
$PY38_BIN/pip install cmake ninja wheel
ln -s $PY38_BIN/cmake /usr/bin/
ln -s $PY38_BIN/ninja /usr/bin/
ln -s $PY38_BIN/wheel /usr/bin/

# Setup python 2.7
yum -y install python-pip
PY27_BIN=/opt/python/cp27-cp27mu/bin
mkdir -p $PY27_BIN
ln -s /usr/bin/python $PY27_BIN/
ln -s /usr/bin/pip $PY27_BIN/
touch $PY27_BIN/python2.7
pip2 install --upgrade pip
pip2 install scikit-build --user

# Upgrade pip and install scikit-build
for PYBIN in /opt/python/*/bin; do
    "$PYBIN"/pip install --upgrade pip
    "$PYBIN"/pip install scikit-build
done
