ARG DIST=18.04
ARG RPKG=robotpkg-py3

FROM memmos.laas.fr:5000/gepetto/buildfarm/$RPKG:$DIST

ARG DIST=18.04

WORKDIR /src
ENV LD_LIBRARY_PATH=/usr/local/lib:/opt/openrobots/lib
USER root

ADD build.sh run.sh build.py /
RUN /build.sh ${DIST} ${PYTHON}

ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh ${DIST} ${PYTHON} eigenpy

ADD https://api.github.com/repos/nim65s/hpp-fcl/commits/topic/multipy2 /
RUN /build.sh ${DIST} ${PYTHON} hpp-fcl

ADD https://api.github.com/repos/nim65s/pinocchio/commits/topic/multipy2 /
RUN /build.sh ${DIST} ${PYTHON} pinocchio

ADD run.py /
CMD /run.sh ${DIST} ${PYTHON}
