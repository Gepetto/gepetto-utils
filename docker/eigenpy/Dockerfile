ARG UBUNTU=focal
FROM ubuntu:$UBUNTU

ENV DEBIAN_FRONTEND=noninteractive CTEST_OUTPUT_ON_FAILURE=true

RUN apt-get update -y \
 && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libeigen3-dev \
 && rm -rf /var/lib/apt/lists/*

ARG EIGENPY=2.2.2

ADD https://github.com/stack-of-tasks/eigenpy/releases/download/v${EIGENPY}/eigenpy-${EIGENPY}.tar.gz /
RUN tar xf /eigenpy-${EIGENPY}.tar.gz \
 && mkdir /eigenpy-${EIGENPY}/build

WORKDIR /eigenpy-${EIGENPY}/build

RUN cmake ..
RUN make
