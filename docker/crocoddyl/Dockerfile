ARG UBUNTU=focal
FROM ubuntu:$UBUNTU

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    assimp-utils \
    build-essential \
    clang-10 \
    cmake \
    curl \
    git \
    libgtest-dev \
    libassimp-dev \
    libboost-all-dev \
    libccd-dev \
    libeigen3-dev \
    liboctomap-dev \
    libtinyxml-dev \
    liburdfdom-dev \
 && rm -rf /var/lib/apt/lists/*

ARG BUILD_TYPE=Release
ARG MAKE_JOBS=6
ENV CTEST_PARALLEL_LEVEL=$MAKE_JOBS CTEST_OUTPUT_ON_FAILURE=true CXX=clang++-10 CC=clang-10
ENV CMAKE_OPTS="-DBUILD_PYTHON_INTERFACE=OFF \
                -DCMAKE_INSTALL_LIBDIR=lib \
                -DCMAKE_INSTALL_PREFIX=/usr \
                -DCMAKE_BUILD_TYPE=${BUILD_TYPE} .."

ARG CPPAD_ORG=coin-or
ARG CPPAD_VER=20200000.2

RUN git clone -b ${CPPAD_VER} --recursive https://github.com/${CPPAD_ORG}/cppad.git \
 && mkdir /cppad/build \
 && cd /cppad/build \
 && cmake ${CMAKE_OPTS} \
 && make -s -j$MAKE_JOBS \
 && make -s install


ARG CPPADCG_ORG=joaoleal
ARG CPPADCG_VER=v2.4.3

RUN git clone -b ${CPPADCG_VER} --recursive https://github.com/${CPPADCG_ORG}/cppadcodegen.git \
 && mkdir /cppadcodegen/build \
 && cd /cppadcodegen/build \
 && cmake ${CMAKE_OPTS} -DGOOGLETEST_GIT=OFF -DUSE_VALGRIND=OFF \
 && make -s -j$MAKE_JOBS \
 && make -s install


ARG HPP_FCL_ORG=humanoid-path-planner
ARG HPP_FCL_VER=v1.4.3

RUN git clone -b ${HPP_FCL_VER} --recursive https://github.com/${HPP_FCL_ORG}/hpp-fcl.git \
 && mkdir /hpp-fcl/build \
 && cd /hpp-fcl/build \
 && cmake ${CMAKE_OPTS} \
 && make -s -j$MAKE_JOBS \
 && make -s test \
 && make -s install


ARG PINOCCHIO_ORG=proyan
ARG PINOCCHIO_VER=forAdria

RUN git clone -b ${PINOCCHIO_VER} --recursive https://github.com/${PINOCCHIO_ORG}/pinocchio.git \
 && mkdir /pinocchio/build \
 && cd /pinocchio/build \
 && cmake ${CMAKE_OPTS} -DBUILD_WITH_COLLISION_SUPPORT=ON \
 && make -s -j$MAKE_JOBS \
 && make -s install


ARG CROCODDYL_ORG=proyan
ARG CROCODDYL_VER=forAdria

RUN git clone -b ${CROCODDYL_VER} --recursive https://github.com/${CROCODDYL_ORG}/crocoddyl.git \
 && mkdir /crocoddyl/build \
 && cd /crocoddyl/build \
 && cmake ${CMAKE_OPTS} \
 && make -s -j$MAKE_JOBS \
 && make -s test \
 && make -s install
