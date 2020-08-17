FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:20.04
WORKDIR /

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh 20.04 python3
CMD /run.sh 20.04 python3
