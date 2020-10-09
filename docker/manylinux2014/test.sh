#!/bin/bash -eu

CP_VERSION="cp$(python -c "import sys; print(''.join(sys.version.split('.')[:2]))")"

while read tgt
do
    echo -e "\n================================ $tgt ===================================\n"
    source "/$tgt/config"
    pip install /"$PACKAGE_NAME"-*-"$CP_VERSION"-*.whl
    python "/$tgt/test.py"
done < targets
