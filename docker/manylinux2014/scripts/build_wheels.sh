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
SKIP_TESTS=$(grep -l BOOST_PYTHON_MODULE "$TEST_DIR"/*.cpp | cut -d'/' -f2 | sed 's/\.cpp/\.py/' | sed 's/^/test_/')
function test {
  python="$1"
  for f in /io/"$TEST_DIR"/python/*.py; do
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
  LD_LIBRARY_PATH="$PWD/_skbuild/linux-x86_64-$PYVERSION/cmake-build:$LD_LIBRARY_PATH" \
    repair_wheel "dist/$(ls -Art dist/ | tail -n 1)"
  rm -rf _skbuild
done


for whl in wheelhouse/*.whl; do
  wheel unpack "$whl"

  # Put the libs inside the package directory so the relative path to the libs is always the same
  mv "${TARGET_NAME//-/_}-$VERSION/${TARGET_NAME//-/_}.libs" "${TARGET_NAME//-/_}-$VERSION/${TARGET_NAME//-/_}-$VERSION.data"/data/lib/python*/site-packages/"$PACKAGE_NAME"/

  # Repair rpath
  patchelf --set-rpath "\$ORIGIN/${TARGET_NAME//-/_}.libs" "${TARGET_NAME//-/_}-$VERSION/${TARGET_NAME//-/_}-$VERSION.data"/data/lib/python*/site-packages/"$PACKAGE_NAME"/*.so
  patchelf --set-rpath '$ORIGIN' "${TARGET_NAME//-/_}-$VERSION/${TARGET_NAME//-/_}-$VERSION.data"/data/lib/python*/site-packages/"$PACKAGE_NAME"/"${TARGET_NAME//-/_}".libs/lib"${PACKAGE_NAME//_/-}"*

  # Remove libraries that are present twice
  rm -rf "${TARGET_NAME//-/_}-$VERSION/${TARGET_NAME//-/_}-$VERSION.data"/data/lib64/*.so

  wheel pack "${TARGET_NAME//-/_}-$VERSION" -d /work/wheelhouse
  rm -rf "${TARGET_NAME//-/_}-$VERSION"/
done

# Install packages and test
for PYBIN in /opt/python/*/bin; do
    "$PYBIN/pip" install "$TARGET_NAME" --no-index --find-links=/work/wheelhouse/
    (cd "$HOME"; test "$PYBIN/python")
done

rm -rf "$TARGET_NAME".egg-info/ dist/

ls /work/wheelhouse
