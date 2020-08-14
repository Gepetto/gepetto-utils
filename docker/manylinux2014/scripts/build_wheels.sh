#!/bin/bash -eu

function repair_wheel {
  wheel="$1"
  if ! auditwheel show "$wheel"; then
    echo "Skipping non-platform wheel $wheel"
  else
    auditwheel repair "$wheel" --plat "$PLAT" -w /io/wheelhouse/
  fi
}

TEST_DIR=$(echo *test*) # Either 'unittest' or 'test' depending on the project
PYTHON_TEST_DIR=$(echo "$TEST_DIR"/python*) # Either 'python' or 'python_unit' depending on the project
SKIP_TESTS=$(grep -l BOOST_PYTHON_MODULE "$TEST_DIR"/*.cpp | cut -d'/' -f2 | sed 's/\.cpp/\.py/' | sed 's/^/test_/')
function test {
  python="$1"
  for f in /io/"$PYTHON_TEST_DIR"/*.py; do
    if ! echo "$SKIP_TESTS" | grep "$(basename "$f")" > /dev/null; then
      printf "\nTesting %s\n" "$f"
      "$python" "$f"
      printf "Ok\n"
    fi
  done
  printf "\n"
}

source config

## Install dependencies
[ -s packages ] && xargs -a packages yum -y install

# Build wheels
for PYBIN in /opt/python/*/bin; do
  PYVERSION=$(find "$PYBIN" -name 'python[0-9]\.[0-9]' -printf "%f\n" | grep -Eo '[0-9].[0-9]')
  [ -n "$INSTALL_REQUIRES" ] && "$PYBIN/pip" install "$(echo "$INSTALL_REQUIRES" | sed -E 's/"|\[|\]|,//g')"
  "$PYBIN/python" setup.py bdist_wheel -- -- -j"$NPROC"

  # Bundle external shared libraries into the wheels
  MAIN_LIB=$(find _skbuild/*/cmake-build -type f ! -path '*test/*' -name 'lib*.so*')
  MAIN_LIB_DIR=$(pwd)/$(dirname "$MAIN_LIB")
  WHEEL_NAME=$(ls -Art dist/ | tail -n 1)

  LD_LIBRARY_PATH="$MAIN_LIB_DIR:$LD_LIBRARY_PATH" \
    repair_wheel "dist/$WHEEL_NAME"
  rm -rf _skbuild
done

for whl in wheelhouse/*.whl; do
  wheel unpack "$whl"

  MAIN_LIB=$(find . -type f ! -path '*.libs/*' ! -path '*lib64/*' -name '*.so*')
  LIB_DIR=$(find . -type d -name '*.libs')
  PACKAGE_DIR=$(dirname "$MAIN_LIB")
  LIB64_DIR=$(find . -type d -name 'lib64')
  WHEEL_DIR=$(echo "$MAIN_LIB" | cut -d'/' -f2)

  # Put the libs inside the package directory so the relative path to the libs is always the same
  mv "$LIB_DIR" "$PACKAGE_DIR"/
  LIB_DIR=$(find . -type d -name '*.libs') # Reassign value because it has changed

  # Change the rpath of the main library so it can find its dependencies
  patchelf --set-rpath "\$ORIGIN/$(basename "$LIB_DIR")" "$MAIN_LIB"

  # Set the rpath of the other shared libraries to LIB_DIR so they can find needed libraries in this directory
  for lib in "$LIB_DIR"/*; do
    patchelf --set-rpath '$ORIGIN' "$lib"
  done

  # Remove libraries that are present twice (auditwheel already copied them in the .libs directory)
  rm -f "$LIB64_DIR"/*.so*

  #TODO: .cmake files should not have references to _skbuild, temporary fix (only for eigenpy.so):
  find "$WHEEL_DIR" -name '*.cmake' | while read -r file; do
    sed -i 's:;/io/_skbuild/linux-x86_64-.*/cmake-install/include::' "$file"
    sed -i 's:/io/_skbuild/linux-x86_64-.*/cmake-install/lib64/libeigenpy.so:/usr/lib/python2.7/site-packages/eigenpy/eigenpy.libs/libeigenpy-453555c1.so:' "$file"
    sed -i 's:libeigenpy.so:libeigenpy-453555c1.so:' "$file"
    sed -i 's:/io/_skbuild/linux-x86_64-.*/cmake-install/include:/usr/local/include:' "$file"
    sed -i 's:/io/_skbuild/linux-x86_64-.*/cmake-install/lib64:/usr/local/lib64:' "$file"
  done

  wheel pack "$WHEEL_DIR" -d /work/wheelhouse
  rm -rf "${WHEEL_DIR:?}"/
done

# Install packages and test
for PYBIN in /opt/python/*/bin; do
    "$PYBIN/pip" install "$TARGET_NAME" --no-index --find-links=/work/wheelhouse/
    (cd "$HOME"; test "$PYBIN/python")
done

rm -rf "$TARGET_NAME".egg-info/ dist/

ls /work/wheelhouse
