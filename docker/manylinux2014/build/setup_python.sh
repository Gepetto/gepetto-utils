#!/bin/bash -eux

rm /opt/python/{cp35-cp35m,cp36-cp36m,cp38-cp38,cp39-cp39}

# Install cmake, ninja and wheel
PY37_BIN=/opt/python/cp37-cp37m/bin
$PY37_BIN/pip install cmake ninja wheel
ln -s $PY37_BIN/cmake /usr/bin/
ln -s $PY37_BIN/ninja /usr/bin/
ln -s $PY37_BIN/wheel /usr/bin/

# Upgrade pip and install scikit-build
for PYBIN in /opt/python/*/bin; do
    "$PYBIN"/pip install --upgrade pip
    "$PYBIN"/pip install scikit-build numpy
done
