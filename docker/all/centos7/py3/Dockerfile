FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:centos7
WORKDIR /

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh centos7 python3
CMD /run.sh centos7 python3
