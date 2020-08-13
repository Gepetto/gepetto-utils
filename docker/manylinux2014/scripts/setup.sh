#!/bin/bash -eu

source config

# Fix CMake for scikit-build
find . -name CMakeLists.txt | xargs sed -i 's/PYTHON_INCLUDE_DIRS/PYTHON_INCLUDE_DIR/'
sed -i 's/REQUIRED COMPONENTS Interpreter Development/REQUIRED COMPONENTS Interpreter/' cmake/python.cmake

# Write setup.py
DESCRIPTION=$(grep PROJECT_DESCRIPTION CMakeLists.txt | cut -d'"' -f2)
for name in TARGET_NAME VERSION DESCRIPTION GIT_URL; do
  var=$(echo "${!name}" | sed 's/\//\\\//g')
  sed -i "s/$name/\"$var\"/" setup.py
done

[ -z "$INSTALL_REQUIRES" ] && sed -i '/INSTALL_REQUIRES/d' setup.py
sed -i "s/INSTALL_REQUIRES/$INSTALL_REQUIRES/" setup.py

python setup.py --help > /dev/null 2>&1 || { echo "Syntax error in config/setup.py, please edit this file."; exit; }

echo -e "\nCurrent setup.py: \n"
cat setup.py
echo -e "\nMake sure that setup.py has the right values before continuing. Then run ./build_wheels.sh\n"
