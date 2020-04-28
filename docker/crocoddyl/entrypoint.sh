#!/bin/bash

lscpu

cd /crocoddyl/build/benchmark/

for bench in bipedal-timings arm-manipulation-cg arm-manipulation-timings bipedal-with-contact-cg
do
    echo
    echo ============ $bench ============
    echo

    eval ./$bench
done
