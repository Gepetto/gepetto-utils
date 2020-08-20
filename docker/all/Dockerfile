ARG DIST=18.04
FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:$DIST

ARG DIST=18.04

WORKDIR /src
ENV LD_LIBRARY_PATH=/usr/local/lib:/opt/openrobots/lib
USER root
RUN echo "DIST=${DIST}" > /dist

ADD build.sh build.py /
ADD dist/${DIST}.sh /dist.sh
RUN bash /dist.sh

ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh eigenpy

ADD https://api.github.com/repos/nim65s/hpp-fcl/commits/topic/multipy2 /
RUN /build.sh hpp-fcl

ADD https://api.github.com/repos/nim65s/pinocchio/commits/topic/multipy2 /
RUN /build.sh pinocchio

ADD run.sh run.py /
CMD /run.sh
