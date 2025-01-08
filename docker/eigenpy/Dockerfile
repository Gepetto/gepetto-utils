FROM ubuntu:noble

ENV CTEST_OUTPUT_ON_FAILURE=true

RUN apt-get update -y \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-all-dev \
    libeigen3-dev \
    python3-numpy \
    python3-scipy \
    python-is-python3 \
 && rm -rf /var/lib/apt/lists/*

ARG EIGENPY=3.10.1

ADD https://github.com/stack-of-tasks/eigenpy/releases/download/v${EIGENPY}/eigenpy-${EIGENPY}.tar.gz /
RUN tar xf /eigenpy-${EIGENPY}.tar.gz


RUN cmake -B build -S /eigenpy-${EIGENPY} -DPYTHON_STANDARD_LAYOUT=ON -DPYTHON_DEB_LAYOUT=ON
RUN cmake --build build -j16
RUN cmake --build build -t test
RUN cmake --build build -t install
RUN python -c "import eigenpy"
