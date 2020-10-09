#!/bin/bash -eux

for PYBIN in /opt/python/*/bin; do
  "$PYBIN/pip" install --find-links=/io/dist/ eigenpy hpp-fcl
done
