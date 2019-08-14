ARG UBUNTU=bionic
FROM ubuntu:$UBUNTU

# Setup Robotpkg apt binary repository
ARG UBUNTU=bionic
RUN apt-get update -y && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
 && echo "deb [arch=amd64] http://robotpkg.openrobots.org/packages/debian/pub $UBUNTU robotpkg" \
 >> /etc/apt/sources.list.d/robotpkg.list \
 && curl http://robotpkg.openrobots.org/packages/debian/robotpkg.key | apt-key add - \
 && rm -rf /var/lib/apt/lists/*

ENV ROBOTPKG_BASE=/opt/openrobots
ENV CMAKE_PREFIX_PATH=$ROBOTPKG_BASE:$CMAKE_PREFIX_PATH \
      LD_LIBRARY_PATH=$ROBOTPKG_BASE/lib:$ROBOTPKG_BASE/lib/plugin:$LD_LIBRARY_PATH \
                 PATH=$ROBOTPKG_BASE/bin:$ROBOTPKG_BASE/sbin:$PATH \
      PKG_CONFIG_PATH=$ROBOTPKG_BASE/lib/pkgconfig:$PKG_CONFIG_PATH \
     ROS_PACKAGE_PATH=$ROBOTPKG_BASE/share:$ROS_PACKAGE_PATH

# get Pinocchio dependencies
ARG PYTHON=python3
RUN apt-get update -y \
 && apt-get install -y \
    $(echo $PYTHON | sed 's/2//') \
 && apt-get install -y \
    libeigen3-dev \
    liburdfdom-dev \
    libtinyxml-dev \
    robotpkg-hpp-fcl \
    robotpkg-py$($PYTHON -V 2>&1 | sed 's/.*\([23]\)\.\([0-9]\).*/\1\2/')-eigenpy \
 && rm -rf /var/lib/apt/lists/*

# (in)validate docker build cache with the HTTP "Last-Modified" header from github
ARG NAMESPACE=stack-of-tasks
ARG BRANCH=devel
ADD https://github.com/$NAMESPACE/pinocchio/archive/$BRANCH.zip .

# but this zip doesn't come with .git nor submodules
RUN git clone --recursive --branch $BRANCH https://github.com/$NAMESPACE/pinocchio.git \
 && mkdir pinocchio/build

WORKDIR /pinocchio/build
ARG MAKE_JOBS=1
RUN cmake -DPYTHON_EXECUTABLE=$(which $PYTHON) .. \
 && make -j$MAKE_JOBS

CMD make test
