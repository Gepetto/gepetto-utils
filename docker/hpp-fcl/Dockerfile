ARG UBUNTU=bionic
FROM ubuntu:$UBUNTU

# Setup Robotpkg apt binary repository
ARG UBUNTU=bionic
ENV UBUNTU=$UBUNTU
RUN apt-get update -y && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
 && echo "deb [arch=amd64] http://robotpkg.openrobots.org/packages/debian/pub $UBUNTU robotpkg" \
 >> /etc/apt/sources.list.d/robotpkg.list \
 && echo "deb [arch=amd64] http://robotpkg.openrobots.org/wip/packages/debian/pub $UBUNTU robotpkg" \
 >> /etc/apt/sources.list.d/robotpkg.list \
 && curl http://robotpkg.openrobots.org/packages/debian/robotpkg.key | apt-key add - \
 && rm -rf /var/lib/apt/lists/*

ENV ROBOTPKG_BASE=/opt/openrobots
ENV CMAKE_PREFIX_PATH=$ROBOTPKG_BASE:$CMAKE_PREFIX_PATH \
      LD_LIBRARY_PATH=$ROBOTPKG_BASE/lib:$ROBOTPKG_BASE/lib/plugin:$LD_LIBRARY_PATH \
                 PATH=$ROBOTPKG_BASE/bin:$ROBOTPKG_BASE/sbin:$PATH \
      PKG_CONFIG_PATH=$ROBOTPKG_BASE/lib/pkgconfig:$PKG_CONFIG_PATH \
     ROS_PACKAGE_PATH=$ROBOTPKG_BASE/share:$ROS_PACKAGE_PATH

# get hpp-fcl dependencies
ARG PYTHON=python3
ENV PYTHON=$PYTHON
RUN apt-get update -y \
 && apt-get install -y \
    $(echo $PYTHON | sed 's/2//') \
 && apt-get install -y \
    libassimp-dev \
    libboost-all-dev \
    robotpkg-octomap \
    robotpkg-py$($PYTHON -V 2>&1 | sed 's/.*\([23]\)\.\([0-9]\).*/\1\2/')-eigenpy \
 && rm -rf /var/lib/apt/lists/*

# (in)validate docker build cache with the HTTP "Last-Modified" header from github
ARG NAMESPACE=humanoid-path-planner
ARG BRANCH=devel
ADD https://api.github.com/repos/${NAMESPACE}/hpp-fcl/commits/${BRANCH} /tmp

RUN git clone --recursive --branch $BRANCH https://github.com/$NAMESPACE/hpp-fcl.git \
 && mkdir hpp-fcl/build

WORKDIR /hpp-fcl/build
ARG MAKE_JOBS=1
ENV CTEST_PARALLEL_LEVEL=$MAKE_JOBS CTEST_OUTPUT_ON_FAILURE=true
RUN cmake -DPYTHON_EXECUTABLE=$(which $PYTHON) .. \
 && make -j$MAKE_JOBS \
 && make test \
 && make install

ENV PYTHONPATH=/usr/local/lib/python3/dist-packages/
