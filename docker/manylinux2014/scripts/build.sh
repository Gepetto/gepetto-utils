#!/bin/bash -eu

# Verify that variables are set properly
source "/work/config/config"
for var in TARGET_NAME PACKAGE_NAME GIT_URL VERSION NPROC; do
  [ -z "${!var}" ] && { echo "$var is not set."; exit; }
done

mkdir -p /work/wheelhouse
[ "$(ls -A /work/wheelhouse)" ] && { echo "./wheelhouse should be empty before running this script."; exit; }

git clone --recursive -j"$NPROC" -b v"$VERSION" "$GIT_URL" /io
cp /work/scripts/* /io
cp /work/config/* /io
./setup.sh
bash
