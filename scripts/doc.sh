#!/bin/bash

# Removes useless folders

set -e

cd /net/cetus/data/gepetto/Doc

for namespace in *; do
    pushd $namespace
    for project in *; do
        pushd $project
        for branch in *; do
            pushd $branch
            for folder in html doxygen-html; do
                [[ -d $folder ]] || continue
                cp -r $folder/* .
                rm -r $folder
            done
            popd
        done
        popd
    done
    popd
done
