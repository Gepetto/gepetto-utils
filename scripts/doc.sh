#!/bin/bash

set -e

cd /net/cetus/data/gepetto/Doc

for namespace in *; do
    pushd $namespace
    for project in *; do
        pushd $project
        for branch in *; do
            pushd $branch
            [[ -d doxygen-html ]] || continue
            cp -r doxygen-html/* .
            rm -r doxygen-html
            popd
        done
        popd
    done
    popd
done
