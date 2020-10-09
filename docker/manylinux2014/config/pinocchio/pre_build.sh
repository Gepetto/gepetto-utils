#!/bin/bash -eux

source "/io/config/hpp-fcl/config"

for PYBIN in /opt/python/*/bin; do
  CP_VERSION="cp$("$PYBIN"/python -c "import sys; print(''.join(sys.version.split('.')[:2]))")"
  #"$PYBIN"/pip install numpy
  "$PYBIN"/pip install /io/dist/eigenpy-*-"$CP_VERSION"-*.whl
  "$PYBIN"/pip install /io/dist/hppfcl-*-"$CP_VERSION"-*.whl
done
