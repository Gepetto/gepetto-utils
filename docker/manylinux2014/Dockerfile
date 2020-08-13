FROM quay.io/pypa/manylinux2014_x86_64:latest

ENV PLAT manylinux2014_x86_64

WORKDIR /build
COPY build/install_boost.sh build/project-config.jam ./
RUN ./install_boost.sh

COPY build/setup_python.sh ./
RUN ./setup_python.sh

WORKDIR /io

CMD ["/bin/bash"]
