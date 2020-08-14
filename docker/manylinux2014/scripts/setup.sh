#!/bin/bash -eu

# Verify that variables are set properly
source "/work/config/config"
for var in TARGET_NAME PACKAGE_NAME GIT_URL VERSION NPROC; do
  [ -z "${!var}" ] && { echo "$var is not set."; exit; }
done

mkdir -p /work/wheelhouse
[ "$(ls -A /work/wheelhouse)" ] && { echo "./wheelhouse should be empty before running this script."; exit; }

git clone --recursive -j"$NPROC" -b v"$VERSION" "$GIT_URL" /io
cp /work/scripts/* /io
cp /work/config/* /io

# Fix CMake for scikit-build
find . -name CMakeLists.txt | xargs sed -i 's/PYTHON_INCLUDE_DIRS/PYTHON_INCLUDE_DIR/'
sed -i 's/REQUIRED COMPONENTS Interpreter Development/REQUIRED COMPONENTS Interpreter/' cmake/python.cmake

# Write setup.py
DESCRIPTION=$(grep PROJECT_DESCRIPTION CMakeLists.txt | cut -d'"' -f2) # TODO: Not working if description on multiple lines
for var in TARGET_NAME VERSION DESCRIPTION GIT_URL; do
  sed -i "s~$var~\"${!var}\"~" setup.py
done

[ -z "$INSTALL_REQUIRES" ] && sed -i '/INSTALL_REQUIRES/d' setup.py
sed -i "s/INSTALL_REQUIRES/$INSTALL_REQUIRES/" setup.py

python setup.py --help > /dev/null 2>&1 || { echo "Syntax error in config/setup.py, please edit this file."; exit; }

./pre_build.sh

echo -e "\nCurrent setup.py: \n"
cat setup.py
echo -e "\nMake sure that setup.py has the right values before continuing. Then run ./build_wheels.sh\n"

bash
