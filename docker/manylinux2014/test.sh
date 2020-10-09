#!/bin/bash -eu

while read tgt
do  echo -e "\n================================ $tgt ===================================\n"
    source "/$tgt/config"
    pip install --find-links=/ "$PACKAGE_NAME"
    python "/$tgt/test.py"
done < targets
