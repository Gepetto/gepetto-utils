#!/bin/bash

set -e

cd /net/cetus/data/gepetto/Doc

for namespace in *; do
    pushd $namespace
    for project in *; do
        pushd $project
        for branch in *; do
            pushd $branch
            [[ -d doc/doxygen-html ]] || continue
            cp -r doc/doxygen-html/* .
            rm -r doc
            popd
        done
        popd
    done
    popd
done
