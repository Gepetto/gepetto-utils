#!/bin/bash -eux

export DIST=$1
export PYTHON=$2
export PROJECT=${3:-main}
export CTEST_PARALLEL_LEVEL=${4:-5}

build() {
    git clone --recursive --depth 1 --branch topic/multipy2 "https://github.com/nim65s/$1.git"
    mkdir "$1/build"
    cd "$1/build" || exit 1
    cmake -DPYTHON_EXECUTABLE="/usr/bin/$PYTHON" -DCMAKE_BUILD_TYPE=Release -DPYTHON_STANDARD_LAYOUT=ON ..
    make -sj"$CTEST_PARALLEL_LEVEL"
    make test
    make install
}

if [ "$PROJECT" = "main" ]
then
    if [ "$DIST" = "archlinux" ] && [ "$PYTHON" = "python2" ]
    then pacman -Sy --noconfirm python2-numpy
    fi
    sed -i "s/python /$PYTHON /" /run.sh
    for p in /usr/local/lib/python*
    do
        mkdir -p "${p}"/dist-packages
        rm -rf "${p}"/site-packages
        ln -s "${p}"/{dist,site}-packages
    done
else
    build "$3"
fi
