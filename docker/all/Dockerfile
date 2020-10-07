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

ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh eigenpy

ADD https://api.github.com/repos/nim65s/hpp-fcl/commits/topic/multipy2 /
RUN /build.sh hpp-fcl

ADD https://api.github.com/repos/nim65s/pinocchio/commits/topic/multipy2 /
RUN /build.sh pinocchio

ADD run.sh run.py /
CMD /run.sh
