FROM quay.io/pypa/manylinux2014_x86_64:latest

ENV PLAT manylinux2014_x86_64

WORKDIR /build

COPY build-wheel/install_boost.sh build-wheel/project-config.jam ./
RUN ./install_boost.sh

COPY build-wheel/setup_python.sh ./
RUN ./setup_python.sh

WORKDIR /io

CMD ["/bin/bash"]
