#!/bin/bash -eu

# Verify that variables are set properly
source "/config/config"
for var in TARGET_NAME PACKAGE_NAME RELEASE_TAG GIT_URL VERSION; do
  [ -z ${!var} ] && { echo "$var is not set."; exit; }
done

 [ "$(ls -A /wheelhouse)" ] && { echo "./wheelhouse should be empty before running this script."; exit; }

git clone --recursive -j"$(nproc)" -b "$RELEASE_TAG" "$GIT_URL" /io
cp /scripts/* /io
cp /config/* /io
./setup.sh
bash
