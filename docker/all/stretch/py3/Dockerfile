FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:stretch
WORKDIR /

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh stretch python3
CMD /run.sh stretch python3
