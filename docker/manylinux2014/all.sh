#!/bin/bash -eux

docker build -t manylinux .
docker run -v "$(pwd -P):/io" -v /local/users/ccache/:/root/.ccache --rm -t manylinux rm -rf /io/dist /io/wheelhouse
docker run -v "$(pwd -P):/io" -v /local/users/ccache/:/root/.ccache --rm -t manylinux /scripts/setup.sh eigenpy
docker run -v "$(pwd -P):/io" -v /local/users/ccache/:/root/.ccache --rm -t manylinux /scripts/setup.sh hpp-fcl
docker run -v "$(pwd -P):/io" -v /local/users/ccache/:/root/.ccache --rm -t manylinux /scripts/setup.sh pinocchio
clear
for PYVER in 2.7 3.5 3.6 3.7 3.8 3.9
do
    docker build -f test.Dockerfile --build-arg PYVER=$PYVER -t manylinux-test:$PYVER .
    docker run --rm -t manylinux-test:$PYVER
done
