#!/bin/bash -eux

yum -y install wget python-devel vim
wget https://dl.bintray.com/boostorg/release/1.74.0/source/boost_1_74_0.tar.bz2
tar --bzip2 -xf boost_1_74_0.tar.bz2
cd boost_1_74_0
./bootstrap.sh --prefix=/usr/local
cp ../project-config.jam .
./b2 install link=shared python=3.7 -j"$(nproc)"
rm -rf /build
