#!/bin/bash

set -ex

lscpu
cat /proc/meminfo

cd /crocoddyl/build/benchmark/

for bench in bipedal-timings arm-manipulation-codegen arm-manipulation-timings bipedal-with-contact-codegen
do
    echo
    echo ============ $bench ============
    echo

    /usr/bin/time -v ./$bench
done
