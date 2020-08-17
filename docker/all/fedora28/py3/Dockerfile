FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:fedora28
WORKDIR /

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh fedora28 python3
CMD /run.sh fedora28 python3
