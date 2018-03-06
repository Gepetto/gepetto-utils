#!/bin/bash

set -x
set -e


TAG=$1
SOFT=${2:-$(basename $(pwd))}
SOFTAG="${SOFT}-${TAG}"

echo Releasing $SOFTAG

rm -vf *.tar* /tmp/*.tar*
git tag -s "v$TAG" -m "Release v$TAG"
if [[ -d cmake && -x cmake/git-archive-all.sh ]]
then
    ./cmake/git-archive-all.sh --prefix "${SOFTAG}/" -v "${SOFTAG}.tar"
    gzip "${SOFTAG}.tar"
else
    git archive --format=tar.gz --prefix="${SOFTAG}/" HEAD > ${SOFTAG}.tar.gz
fi
gpg --armor --detach-sign "${SOFTAG}.tar.gz"

echo -e "git push --tags
git log --pretty=oneline $(git tag -l|tail -n2|sed ':a;N;$!ba;s/\n/../g') | sed 's/.\{48\}/*/'
# Draft new release"
