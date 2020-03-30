#!/bin/bash

# Usage: ./release.sh version [pkg_name] [revision]
# pkg_name defaults to the name of the current working directory
# eg.: ./release.sh 0.8.1

set -ex

TAG=$1
SOFT=${2:-$(basename $(pwd))}
SOFTAG="${SOFT}-${TAG}"
[[ $# -gt 2 ]] && SOFTAG="${SOFTAG}r$2"

echo Releasing $SOFTAG

rm -vf ${SOFTAG}.tar*

if $(grep -q "v$TAG" <<< $(git tag))
then
    echo -e "\n!!! This tag exists !!!\n"
    git checkout "v$TAG"
    git submodule update --init
else
    git tag -s "v$TAG" -m "Release v$TAG"
fi

if [[ -d cmake && -x cmake/git-archive-all.sh ]]
then
    ./cmake/git-archive-all.sh --prefix "${SOFTAG}/" -v "${SOFTAG}.tar"
else
    git archive --format=tar --prefix="${SOFTAG}/" "v$TAG" > ${SOFTAG}.tar
fi

echo $TAG > .version
tar rf "${SOFTAG}.tar" --transform "s=.=${SOFTAG}/.="   .version
gzip "${SOFTAG}.tar"

gpg --armor --detach-sign "${SOFTAG}.tar.gz"
[[ -f "${SOFTAG}.tar.gz.asc" ]] && mv "${SOFTAG}.tar.gz.asc" "${SOFTAG}.tar.gz.sig"

rm .version
mkdir -p build
mv "${SOFTAG}"* build/
