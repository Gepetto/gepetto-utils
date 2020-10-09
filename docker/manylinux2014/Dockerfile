FROM memmos.laas.fr:5000/gepetto/buildfarm/robotpkg:centos7 as build

ADD config/robotpkg /
RUN while read pkg ; do make -C $pkg install; done < /robotpkg; \
    rm -rf $(find . -name work.$HOSTNAME)

FROM quay.io/pypa/manylinux2014_x86_64:latest

ENV PLAT manylinux2014_x86_64

WORKDIR /build
COPY build/install_boost.sh build/project-config.jam ./
RUN ./install_boost.sh

COPY build/setup_python.sh ./
RUN ./setup_python.sh

ADD config/packages /
RUN yum install -y $(cat /packages)
ENV CXX="ccache g++" CC="ccache gcc"

WORKDIR /src

ADD scripts /scripts
CMD ["/bin/bash"]

COPY --from=build /opt/openrobots /opt/openrobots
