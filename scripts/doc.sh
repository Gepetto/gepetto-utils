#!/bin/bash

# Removes useless folders, and set permissions

set -e

cd /net/pongo/vol/vol_projects/partage_gepetto/Doc

for namespace in *; do
    [[ -d $namespace ]] || continue
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

find . -type d -exec chmod 0775 {} \;
find . -type f -exec chmod 0664 {} \;
