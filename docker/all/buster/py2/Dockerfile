FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg:buster
WORKDIR /

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh buster python2
CMD /run.sh buster python2
