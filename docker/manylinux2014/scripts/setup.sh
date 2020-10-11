#!/bin/bash -eux

TARGET=${1:-eigenpy}
PYVER=${2:-3.9}

URL="$(grep url "/io/config/$TARGET/setup.py" | cut -d'"' -f2)"
VERSION="$(curl -sSL "$(echo $URL | sed 's:github.com:api.github.com/repos:')/releases/latest" | grep tag_name | sed 's/[^.0-9]//g')"

mkdir -p /io/wheelhouse
[ "$(ls -A /io/wheelhouse)" ] && { echo "./wheelhouse should be empty before running this script."; exit; }

curl -sSL "$URL/releases/download/v$VERSION/$TARGET-$VERSION.tar.gz" \
    | tar xz --strip-components=1 2> /dev/null

cp "/io/config/$TARGET/setup.py" .
cp /scripts/pyproject.toml .

# Fix CMake for scikit-build
find . -name CMakeLists.txt | xargs sed -i 's/PYTHON_INCLUDE_DIRS/PYTHON_INCLUDE_DIR/'
sed -i 's/REQUIRED COMPONENTS Interpreter Development/REQUIRED COMPONENTS Interpreter/' cmake/python.cmake

/scripts/build_wheels.sh "$TARGET" "$PYVER"
