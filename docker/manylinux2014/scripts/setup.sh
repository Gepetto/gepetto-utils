set -eux

# Verify that variables are set properly
source "${BASH_SOURCE%/*}/.env"
for var in TARGET_NAME RELEASE_URL VERSION; do
  [ -z ${!var} ] && { echo "$var is not set."; exit; }
done

# Fix CMake for scikit-build
#find . -name CMakeLists.txt | xargs sed -i 's/PYTHON_INCLUDE_DIRS/PYTHON_INCLUDE_DIR/'
#sed -i 's/REQUIRED COMPONENTS Interpreter Development/REQUIRED COMPONENTS Interpreter/' cmake/python.cmake

# Write setup.py
DESCRIPTION=$(grep PROJECT_DESCRIPTION CMakeLists.txt | cut -d'"' -f2)
URL=$(grep PROJECT_URL CMakeLists.txt | cut -d'"' -f2)
for var in TARGET_NAME VERSION DESCRIPTION URL; do
  sed -i "s/$var/\"${!var}\"/" setup.py
done
sed -i "s/INSTALL_REQUIRES/$INSTALL_REQUIRES/" setup.py

#python setup.py --help > /dev/null 2>&1 || { echo "Syntax error in config/setup.py, please edit this file."; exit; }


echo "Setup done."
echo "Make sure that setup.py has the right values before continuing."