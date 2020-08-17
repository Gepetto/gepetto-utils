FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg:centos7
WORKDIR /

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh centos7 python2
CMD /run.sh centos7 python2
