FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg:18.04
WORKDIR /

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh 18.04 python2
CMD /run.sh 18.04 python2
