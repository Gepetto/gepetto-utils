#!/bin/bash -eux

BOOST_VERSION="1_74_0"

yum install -q -y which wget
yum erase -q -y boost-libs boost-devel boost-python36-devel python2-numpy numpy

wget -q https://dl.bintray.com/boostorg/release/${BOOST_VERSION//_/.}/source/boost_${BOOST_VERSION}.tar.bz2
tar xf boost_${BOOST_VERSION}.tar.bz2
cd boost_${BOOST_VERSION}
./bootstrap.sh --prefix=/usr/local
patch << 'EOF'
--- project-config.jam  2020-08-20 11:38:06.896289775 +0000
+++ project-confi.jam  2020-08-20 11:37:48.052239309 +0000
@@ -18,7 +18,8 @@
 import python ;
 if ! [ python.configured ]
 {
-    using python : 2.7 : "/usr" ;
+    using python : 2.7 : /usr/bin/python2 : /usr/include/python2.7 : /usr/lib ;
+    using python : 3.6 : /usr/bin/python3 : /usr/include/python3.6m : /usr/lib ;
 }

 # List of --with-<library> and --without-<library>
EOF
./b2 install link=shared python=2.7,3.6
echo /opt/openrobots/lib/python2.7/site-packages/ > /usr/lib/python2.7/site-packages/robotpkg.pth

python2 -m pip install -U numpy
python3 -m pip install -U numpy

make -C ~/robotpkg/graphics/urdfdom install

rm -rf /src/boost_${BOOST_VERSION}
