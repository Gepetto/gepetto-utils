#!/bin/bash -eux

TARGET=${1:-eigenpy}

# Verify that variables are set properly
source "/io/config/$TARGET/config"
for var in PACKAGE_NAME GITHUB_ORG VERSION NPROC; do
  [ -z "${!var}" ] && { echo "$var is not set."; exit; }
done

mkdir -p /io/wheelhouse
[ "$(ls -A /io/wheelhouse)" ] && { echo "./wheelhouse should be empty before running this script."; exit; }

curl -sSL "https://github.com/$GITHUB_ORG/$TARGET/releases/download/v$VERSION/$TARGET-$VERSION.tar.gz" \
    | tar xz --strip-components=1 2> /dev/null

cp /scripts/setup.py .

# Fix CMake for scikit-build
find . -name CMakeLists.txt | xargs sed -i 's/PYTHON_INCLUDE_DIRS/PYTHON_INCLUDE_DIR/'
sed -i 's/REQUIRED COMPONENTS Interpreter Development/REQUIRED COMPONENTS Interpreter/' cmake/python.cmake

# Write setup.py
DESCRIPTION=$(grep PROJECT_DESCRIPTION CMakeLists.txt | cut -d'"' -f2) # TODO: Not working on multiple lines
for var in PACKAGE_NAME GITHUB_ORG TARGET VERSION DESCRIPTION; do
  sed -i "s~$var~${!var}~" setup.py
done

[ -z "$INSTALL_REQUIRES" ] && sed -i '/INSTALL_REQUIRES/d' setup.py
sed -i "s/INSTALL_REQUIRES/$INSTALL_REQUIRES/" setup.py

cat setup.py

python setup.py --help || { echo "Syntax error in config/setup.py, please edit this file."; exit; }

echo -e "\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"

[ -x "/io/config/$TARGET/pre_build.sh" ] && "/io/config/$TARGET/pre_build.sh" "$TARGET"

echo -e "\n=========================================================================================================\n"

/scripts/build_wheels.sh "$TARGET"
