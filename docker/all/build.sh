#!/bin/bash -eux

export DIST=$1
export PYTHON=$2
export PROJECT=${3:-main}
export CTEST_PARALLEL_LEVEL=${4:-5}

build() {
    git clone --recursive --depth 1 --branch topic/multipy2 "https://github.com/nim65s/$1.git"
    mkdir "$1/build"
    cd "$1/build" || exit 1
    cmake -DPYTHON_EXECUTABLE="/usr/bin/$PYTHON" -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DCMAKE_CXX_STANDARD=11 .. \
        -DPYTHON_STANDARD_LAYOUT=ON -DCMAKE_INSTALL_PREFIX=/opt/openrobots -DCMAKE_INSTALL_LIBDIR=lib
    make -sj"$CTEST_PARALLEL_LEVEL"
    # make test TODO: hpp-fcl tests are failing for many platforms
    make install
}

if [ "$PROJECT" = "main" ]
then
    if [ "$DIST" = "archlinux" ] && [ "$PYTHON" = "python2" ]
    then pacman -Sy --noconfirm python2-numpy
    fi
    if [ "$DIST" = "centos7" ]
    then
        $PYTHON -m pip install cmake
        yum install -q -y python3-devel python3-numpy boost-python36-devel
    fi
    sed -i "s/python /$PYTHON /" /run.sh
else
    build "$3"
fi
