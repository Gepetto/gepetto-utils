#!/bin/bash -eux

pyver=${1:-all}

docker build -t manylinux .
docker run -v "$(pwd -P):/io" -v /local/users/ccache/:/root/.ccache --rm -t manylinux rm -rf /io/dist /io/wheelhouse

build() {
    for target in eigenpy hpp-fcl pinocchio
    do docker run -v "$(pwd -P):/io" -v /local/users/ccache/:/root/.ccache --rm -t manylinux /scripts/setup.sh $target $1
    done
}

test() {
    docker build -f test.Dockerfile --build-arg PYVER=$pyver -t manylinux-test:$pyver .
    docker run --rm -t manylinux-test:$pyver
}

if [ "$pyver" = all ]
then
    for pyver in 2.7 3.5 3.6 3.7 3.8 3.9
    do build $pyver
    done
    wait
else
    build $pyver
fi

clear

if [ "$pyver" = all ]
then
    for pyver in 2.7 3.5 3.6 3.7 3.8 3.9
    do test $pyver
    done
else
    test $pyver
fi
