#!/bin/bash

set -x
set -e

[[ -x cmake/git-archive-all.sh ]]

TAG=$1
SOFT=${2:-$(basename $(pwd))}

echo Releasing $SOFT $TAG

rm -vf *.tar* /tmp/*.tar*
git tag -u $KEY -s "v$TAG" -m "Release v$TAG"
./cmake/git-archive-all.sh --prefix "${SOFT}-${TAG}/" -v "${SOFT}-${TAG}.tar"
gzip "${SOFT}-${TAG}.tar"
gpg --armor --detach-sign "${SOFT}-${TAG}.tar.gz"
git push --tags
