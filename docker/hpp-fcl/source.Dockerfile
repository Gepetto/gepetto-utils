FROM ubuntu:16.04

ARG EIGENPY_VERSION=2.4.3
ADD https://github.com/stack-of-tasks/eigenpy/releases/download/v${EIGENPY_VERSION}/eigenpy-${EIGENPY_VERSION}.tar.gz /
ARG HPP_FCL_VERSION=1.4.6
ADD https://github.com/humanoid-path-planner/hpp-fcl/releases/download/v${HPP_FCL_VERSION}/hpp-fcl-${HPP_FCL_VERSION}.tar.gz /

RUN apt-get update -qqy \
 && apt-get install -qqy \
    build-essential \
    cmake \
    libassimp-dev \
    libboost-all-dev \
    libeigen3-dev \
    liboctomap-dev \
    libpython3-dev \
    python3-numpy \
 && rm -rf /var/lib/apt/lists/*

RUN tar xvf /eigenpy-${EIGENPY_VERSION}.tar.gz \
 && tar xvf /hpp-fcl-${HPP_FCL_VERSION}.tar.gz

WORKDIR /eigenpy-${EIGENPY_VERSION}/build

ENV CTEST_OUTPUT_ON_FAILURE=1 CTEST_PARALLEL_LEVEL=12

ADD https://github.com/jrl-umi3218/jrl-cmakemodules/commit/43806fd9c1b85480e6fcbd3968a36c3c23345d12.patch /patch
RUN cd ../cmake \
 && patch -p1 -i /patch


RUN cmake -DPYTHON_EXECUTABLE=/usr/bin/python3 .. \
 && make -sj12 \
 && make test \
 && make install

#WORKDIR /hpp-fcl-${HPP_FCL_VERSION}/build

## TODO: doesn't work.
## ref https://github.com/jrl-umi3218/jrl-cmakemodules/issues/422
RUN cmake -DPYTHON_EXECUTABLE=/usr/bin/python3 .. \
 && make -sj12 \
 && make test \
 && make install
