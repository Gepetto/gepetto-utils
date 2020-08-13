#!/bin/bash -eux

yum -y install wget python-devel
wget https://dl.bintray.com/boostorg/release/1.72.0/source/boost_1_72_0.tar.bz2
tar --bzip2 -xf boost_1_72_0.tar.bz2
cd boost_1_72_0
./bootstrap.sh --prefix=/usr/local
cp ../project-config.jam .
./b2 install link=shared python=2.7,3.5,3.6,3.7,3.8 --with-python --with-test -j"$(nproc)"
rm -rf /build
