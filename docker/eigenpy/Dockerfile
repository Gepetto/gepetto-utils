FROM ubuntu:focal

ENV CTEST_OUTPUT_ON_FAILURE=true

RUN apt-get update -y \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-all-dev \
    libeigen3-dev \
    python3-numpy \
    python-is-python3 \
 && rm -rf /var/lib/apt/lists/*

ARG EIGENPY=2.6.4

ADD https://github.com/stack-of-tasks/eigenpy/releases/download/v${EIGENPY}/eigenpy-${EIGENPY}.tar.gz /
RUN tar xf /eigenpy-${EIGENPY}.tar.gz

WORKDIR /eigenpy-${EIGENPY}/build

RUN cmake ..
