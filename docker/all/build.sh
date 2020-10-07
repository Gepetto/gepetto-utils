#!/bin/bash -eux

source /dist

export PROJECT=$1

DO_TEST=true
if [ "$PROJECT" = "hpp-fcl" ]
then
    if [[ "$DIST" = "fedora28" || "$DIST" = "fedora31" || "$DIST" = "buster" ]]
    then DO_TEST=false
    fi
fi

build() {
    git clone --recursive --depth 1 --branch topic/multipy "https://github.com/nim65s/$PROJECT.git"
    mkdir "$PROJECT"/build{,2,3}
    cd "/src/$PROJECT/build" || exit 1
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=ON -DCMAKE_CXX_STANDARD=11 -DINSTALL_DOCUMENTATION=OFF \
        -DCMAKE_INSTALL_PREFIX=/opt/openrobots -DCMAKE_INSTALL_LIBDIR=lib \
        -DBUILD_PYTHON_INTERFACE=OFF ..
    make -sj"$CTEST_PARALLEL_LEVEL"
    DO_TEST && make test
    make install

    if [ "$DIST" != "20.04" ]
    then
        cd "../build2" || exit 1
        cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=ON -DCMAKE_CXX_STANDARD=11 -DINSTALL_DOCUMENTATION=OFF \
            -DCMAKE_INSTALL_PREFIX=/opt/openrobots -DCMAKE_INSTALL_LIBDIR=lib \
            -DPYTHON_EXECUTABLE="/usr/bin/python2" -DPYTHON_STANDARD_LAYOUT=ON -DINSTALL_PYTHON_INTERFACE_ONLY=ON ..
        make -sj"$CTEST_PARALLEL_LEVEL"
        DO_TEST && make test
        make install
    fi

    cd "../build3" || exit 1
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=ON -DCMAKE_CXX_STANDARD=11 -DINSTALL_DOCUMENTATION=OFF \
        -DCMAKE_INSTALL_PREFIX=/opt/openrobots -DCMAKE_INSTALL_LIBDIR=lib \
        -DPYTHON_EXECUTABLE="/usr/bin/python3" -DPYTHON_STANDARD_LAYOUT=ON -DINSTALL_PYTHON_INTERFACE_ONLY=ON ..
    make -sj"$CTEST_PARALLEL_LEVEL"
    DO_TEST && make test
    make install
}

if [ "$DIST" = "centos7" ]
then export PATH=/usr/lib64/python2.7/site-packages/cmake/data/bin:$PATH
fi

build "$PROJECT"
