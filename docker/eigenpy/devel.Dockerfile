FROM ubuntu:focal

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

RUN git clone --recursive -b devel https://github.com/stack-of-tasks/eigenpy.git

WORKDIR eigenpy/build

RUN cmake ..

#RUN make -sj16
