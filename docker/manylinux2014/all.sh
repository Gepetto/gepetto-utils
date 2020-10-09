#!/bin/bash -eux

sudo touch dist wheelhouse
sudo rm -rf dist wheelhouse
docker build -t manylinux .
docker run -v "$(pwd -P):/io" -t manylinux /scripts/setup.sh eigenpy
docker run -v "$(pwd -P):/io" -t manylinux /scripts/setup.sh hpp-fcl
docker run -v "$(pwd -P):/io" -t manylinux /scripts/setup.sh pinocchio
docker build -f test.Dockerfile -t manylinux-test .
docker run --rm -t manylinux-test
