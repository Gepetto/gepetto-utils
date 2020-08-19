#!/bin/bash -eux

source /dist

export PROJECT=${1:-main}
export CTEST_PARALLEL_LEVEL=${2:-5}

build() {
    git clone --recursive --depth 1 --branch topic/multipy2 "https://github.com/nim65s/$1.git"
    mkdir "$1"/build{,2,3}
    cd "/src/$1/build" || exit 1
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DCMAKE_CXX_STANDARD=11 \
        -DCMAKE_INSTALL_PREFIX=/opt/openrobots -DCMAKE_INSTALL_LIBDIR=lib \
        -DBUILD_PYTHON_INTERFACE=OFF ..
    make -sj"$CTEST_PARALLEL_LEVEL"
    # make test TODO: hpp-fcl tests are failing for many platforms
    make install

    cd "../build2" || exit 1
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DCMAKE_CXX_STANDARD=11 \
        -DCMAKE_INSTALL_PREFIX=/opt/openrobots -DCMAKE_INSTALL_LIBDIR=lib \
        -DPYTHON_EXECUTABLE="/usr/bin/python2" -DPYTHON_STANDARD_LAYOUT=ON -DINSTALL_PYTHON_INTERFACE_ONLY=ON ..
    make -sj"$CTEST_PARALLEL_LEVEL"
    # make test TODO: hpp-fcl tests are failing for many platforms
    make install

    cd "../build3" || exit 1
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DCMAKE_CXX_STANDARD=11 \
        -DCMAKE_INSTALL_PREFIX=/opt/openrobots -DCMAKE_INSTALL_LIBDIR=lib \
        -DPYTHON_EXECUTABLE="/usr/bin/python3" -DPYTHON_STANDARD_LAYOUT=ON -DINSTALL_PYTHON_INTERFACE_ONLY=ON ..
    make -sj"$CTEST_PARALLEL_LEVEL"
    # make test TODO: hpp-fcl tests are failing for many platforms
    make install
}

if [ "$PROJECT" = "main" ]
then
    if [ "$DIST" = "archlinux" ]
    then pacman -Sy --noconfirm python2-numpy
    fi
    if [ "$DIST" = "centos7" ]
    then make -C ~/robotpkg/graphics/urdfdom install
    fi
else
    if [ "$DIST" = "centos7" ]
    then export PATH=/usr/lib64/python2.7/site-packages/cmake/data/bin:$PATH
    fi
    build "$PROJECT"
fi
