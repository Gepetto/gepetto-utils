ARG DIST=18.04
FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:$DIST as build

RUN for dep in math/eiquadprog; do \
    make install -C $dep; \
    make clean -C $dep; \
    done

ARG DIST=18.04
FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:$DIST

WORKDIR /src
USER root

ARG DIST=18.04
RUN echo "DIST=${DIST}" > /dist

ADD build.sh build.py /
ADD dist/${DIST}.sh /dist.sh
RUN bash /dist.sh

ARG PARALLEL=1
ENV CTEST_PARALLEL_LEVEL=${PARALLEL}

ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy /
RUN /build.sh eigenpy

ADD https://api.github.com/repos/nim65s/hpp-fcl/commits/topic/multipy /
RUN /build.sh hpp-fcl

ADD https://api.github.com/repos/nim65s/pinocchio/commits/topic/multipy /
RUN /build.sh pinocchio

ADD https://api.github.com/repos/nim65s/example-robot-data/commits/topic/multipy /
RUN /build.sh example-robot-data

ADD https://api.github.com/repos/nim65s/curves/commits/topic/multipy /
RUN /build.sh curves

ADD https://api.github.com/repos/nim65s/multicontact-api/commits/topic/multipy /
RUN /build.sh multicontact-api

COPY --from=build /opt/openrobots /opt/openrobots

ADD https://api.github.com/repos/nim65s/tsid/commits/topic/multipy /
RUN /build.sh tsid

ADD https://api.github.com/repos/nim65s/crocoddyl/commits/topic/multipy /
RUN /build.sh crocoddyl

ADD run.sh run.py /
CMD /run.sh
