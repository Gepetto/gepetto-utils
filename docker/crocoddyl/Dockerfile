ARG UBUNTU=focal
FROM ubuntu:$UBUNTU as main

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
    time \
 && rm -rf /var/lib/apt/lists/*

RUN git config --global advice.detachedHead false

ARG BUILD_TYPE=Release
ARG MAKE_JOBS=6
ENV CTEST_PARALLEL_LEVEL=$MAKE_JOBS CTEST_OUTPUT_ON_FAILURE=true CXX=clang++-10 CC=clang-10
ENV CMAKE_OPTS="-DBUILD_PYTHON_INTERFACE=OFF \
                -DCMAKE_INSTALL_LIBDIR=lib \
                -DCMAKE_INSTALL_PREFIX=/usr \
                -DCMAKE_BUILD_TYPE=${BUILD_TYPE} .."


FROM main as cppad

ARG CPPAD_ORG=coin-or
ARG CPPAD_VER=20200000.2

ADD https://api.github.com/repos/${CPPAD_ORG}/cppad/commits/${CPPAD_VER} /tmp
RUN git clone -b ${CPPAD_VER} --recursive https://github.com/${CPPAD_ORG}/cppad.git
WORKDIR /cppad/build
RUN cmake ${CMAKE_OPTS}
RUN make -s -j$MAKE_JOBS
RUN make -s install


FROM main as cppadcg

COPY --from=cppad /usr /usr

ARG CPPADCG_ORG=joaoleal
ARG CPPADCG_VER=v2.4.3

ADD https://api.github.com/repos/${CPPADCG_ORG}/cppadcodegen/commits/${CPPADCG_VER} /tmp
RUN git clone -b ${CPPADCG_VER} --recursive https://github.com/${CPPADCG_ORG}/cppadcodegen.git
WORKDIR /cppadcodegen/build
RUN cmake ${CMAKE_OPTS} -DGOOGLETEST_GIT=OFF -DUSE_VALGRIND=OFF
RUN make -s -j$MAKE_JOBS
RUN make -s install


FROM main as hpp-fcl

ARG HPP_FCL_ORG=humanoid-path-planner
ARG HPP_FCL_VER=v1.4.3

ADD https://api.github.com/repos/${HPP_FCL_ORG}/hpp-fcl/commits/${HPP_FCL_VER} /tmp
RUN git clone -b ${HPP_FCL_VER} --recursive https://github.com/${HPP_FCL_ORG}/hpp-fcl.git
WORKDIR /hpp-fcl/build
RUN cmake ${CMAKE_OPTS}
RUN make -s -j$MAKE_JOBS
RUN make -s test
RUN make -s install


FROM main as pinocchio

COPY --from=hpp-fcl /usr /usr
COPY --from=cppadcg /usr /usr

ARG PINOCCHIO_ORG=stack-of-tasks
ARG PINOCCHIO_VER=v2.4.3

ADD https://api.github.com/repos/${PINOCCHIO_ORG}/pinocchio/commits/${PINOCCHIO_VER} /tmp
RUN git clone -b ${PINOCCHIO_VER} --recursive https://github.com/${PINOCCHIO_ORG}/pinocchio.git
WORKDIR /pinocchio/build
RUN cmake ${CMAKE_OPTS} -DBUILD_WITH_COLLISION_SUPPORT=ON -DBUILD_WITH_CODEGEN_SUPPORT=ON -D-DBUILD_WITH_AUTODIFF_SUPPORT=ON
RUN make -s -j$MAKE_JOBS
RUN make -s install

RUN sed -i 's=;/usr/\.\./include/include==' /usr/lib/cmake/pinocchio/pinocchioTargets.cmake


FROM main as example-robot-data

ARG EXAMPLE_ROBOT_DATA_ORG=gepetto
ARG EXAMPLE_ROBOT_DATA_VER=v3.2.0

ADD https://api.github.com/repos/${EXAMPLE_ROBOT_DATA_ORG}/example-robot-data/commits/${EXAMPLE_ROBOT_DATA_VER} /tmp
RUN git clone -b ${EXAMPLE_ROBOT_DATA_VER} --recursive https://github.com/${EXAMPLE_ROBOT_DATA_ORG}/example-robot-data.git
WORKDIR /example-robot-data/build
RUN cmake ${CMAKE_OPTS}
RUN make -s -j$MAKE_JOBS
RUN make -s test
RUN make -s install


FROM main as crocoddyl

COPY --from=cppadcg /usr /usr
COPY --from=pinocchio /usr /usr
COPY --from=example-robot-data /usr /usr

ARG CROCODDYL_ORG=proyan
ARG CROCODDYL_VER=forAdria

ADD https://api.github.com/repos/${CROCODDYL_ORG}/crocoddyl/commits/${CROCODDYL_VER} /tmp
RUN git clone -b ${CROCODDYL_VER} --recursive https://github.com/${CROCODDYL_ORG}/crocoddyl.git
WORKDIR /crocoddyl/build
RUN cmake ${CMAKE_OPTS}
RUN make -s
RUN make -s test
RUN make -s install

ADD entrypoint.sh /usr/local

CMD /usr/local/entrypoint.sh
