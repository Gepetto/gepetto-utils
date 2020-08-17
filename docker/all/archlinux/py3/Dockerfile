FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg-py3:archlinux
WORKDIR /
USER root

ADD build.sh run.sh /
ADD https://api.github.com/repos/nim65s/eigenpy/commits/topic/multipy2 /
RUN /build.sh archlinux python3
CMD /run.sh archlinux python3
