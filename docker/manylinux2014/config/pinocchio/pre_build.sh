#!/bin/bash -eux

source "/io/config/hpp-fcl/config"

for PYBIN in /opt/python/*/bin; do
  "$PYBIN/pip" install --find-links=/io/dist/ eigenpy hpp-fcl
done
