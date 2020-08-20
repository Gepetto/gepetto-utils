#!/bin/bash -eux

BOOST_VERSION="1_72_0"

wget https://dl.bintray.com/boostorg/release/${BOOST_VERSION//_/.}/source/boost_${BOOST_VERSION}.tar.bz2
tar xvf boost_${BOOST_VERSION}.tar.bz2
cd boost_${BOOST_VERSION}
./bootstrap.sh --prefix=/usr/local
#cp ../project-config.jam .
./b2 install link=shared python=2.7,3.6
rm -rf /src/boost
