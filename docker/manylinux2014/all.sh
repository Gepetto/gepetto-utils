#!/bin/bash -eux

pyver="${1:-all}"
pwd="$(pwd -P)"

docker build -t manylinux .
docker run -v "$pwd:/io" -v /local/users/ccache/:/root/.ccache --rm -t manylinux rm -rf /io/dist /io/wheelhouse

build_wheel() {
    while read target
    do docker run -v "$pwd:/io" -v /local/users/ccache/:/root/.ccache --rm -t manylinux /scripts/setup.sh $target $1
    done < config/targets
}

test_wheel() {
    docker build -f test.Dockerfile --build-arg PYVER=$1 -t manylinux-test:$1 .
    docker run --rm -t manylinux-test:$1
}

if [ "$pyver" = all ]
then
    for pv in 2.7 3.5 3.6 3.7 3.8 3.9
    do build_wheel $pv
    done
else
    build_wheel $pyver
fi

clear

if [ "$pyver" = all ]
then
    for pv in 2.7 3.5 3.6 3.7 3.8 3.9
    do test_wheel $pv
    done
else
    test_wheel $pyver
fi
