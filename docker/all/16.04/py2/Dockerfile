FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg:16.04
WORKDIR /

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh 16.04 python2
CMD /run.sh 16.04 python2
