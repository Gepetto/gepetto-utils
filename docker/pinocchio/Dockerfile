FROM ubuntu:focal

# Setup Robotpkg apt binary repository
ADD http://robotpkg.openrobots.org/packages/debian/robotpkg.key /
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt-get update -qqy && DEBIAN_FRONTEND=noninteractive apt-get install -qqy gnupg2 \
 && apt-key add /robotpkg.key \
 && echo "deb [arch=amd64] http://robotpkg.openrobots.org/packages/debian/pub focal robotpkg\n" \
         "deb [arch=amd64] http://robotpkg.openrobots.org/wip/packages/debian/pub focal robotpkg\n" \
 >> /etc/apt/sources.list.d/robotpkg.list

# get Pinocchio dependencies
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt-get update -qqy && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    build-essential \
    ccache \
    cmake \
    git \
    libeigen3-dev \
    liburdfdom-dev \
    libtinyxml-dev \
    python-is-python3 \
    robotpkg-cppadcodegen \
    robotpkg-py38-casadi \
    robotpkg-py38-hpp-fcl

# Configure python path
RUN echo "/opt/openrobots/lib/python3.8/site-packages" >> /usr/lib/python3/dist-packages/robotpkg.pth

# (in)validate docker build cache with the HTTP "Last-Modified" header from github
ARG ORG=stack-of-tasks
ARG BRANCH=devel
ADD https://api.github.com/repos/${ORG}/pinocchio/commits/${BRANCH} .

RUN git clone --recursive --branch $BRANCH -j4 https://github.com/$ORG/pinocchio.git

WORKDIR /pinocchio/build
ARG MAKE_JOBS=1
ENV CCACHE_DIR=/ccache CMAKE_PREFIX_PATH=/opt/openrobots \
    CTEST_PARALLEL_LEVEL=$MAKE_JOBS CTEST_OUTPUT_ON_FAILURE=true

RUN --mount=type=cache,target=/ccache cmake -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
                                            -DBUILD_ADVANCED_TESTING=ON \
                                            -DBUILD_BENCHMARK=ON \
                                            -DBUILD_UTILS=ON \
                                            -DBUILD_WITH_AUTODIFF_SUPPORT=ON \
                                            -DBUILD_WITH_CASADI_SUPPORT=ON \
                                            -DBUILD_WITH_CODEGEN_SUPPORT=ON \
                                            -DBUILD_WITH_COLLISION_SUPPORT=ON \
                                            -DBUILD_WITH_OPENMP_SUPPORT=ON \
                                            -DLINK_PYTHON_INTERFACE_TO_OPENM=ON \
                                            ..
RUN --mount=type=cache,target=/ccache make -sj$MAKE_JOBS
RUN make test
RUN make install
