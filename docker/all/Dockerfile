ARG DIST=18.04
FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:$DIST

ARG DIST=18.04

WORKDIR /src
ENV LD_LIBRARY_PATH=/usr/local/lib:/opt/openrobots/lib
USER root

ADD build.sh run.sh build.py /
RUN /build.sh ${DIST}

ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh ${DIST} eigenpy

ADD https://api.github.com/repos/nim65s/hpp-fcl/commits/topic/multipy2 /
RUN /build.sh ${DIST} hpp-fcl

ADD https://api.github.com/repos/nim65s/pinocchio/commits/topic/multipy2 /
RUN /build.sh ${DIST} pinocchio

ADD run.py /
CMD /run.sh ${DIST}
