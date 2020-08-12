#!/bin/bash -eu

function repair_wheel {
  wheel="$1"
  if ! auditwheel show "$wheel"; then
    echo "Skipping non-platform wheel $wheel"
  else
    auditwheel repair "$wheel" --plat "$PLAT" -w /io/wheelhouse/
  fi
}

SKIP_TESTS=$(grep -l BOOST_PYTHON_MODULE unittest/*.cpp | cut -d'/' -f2 | sed 's/\.cpp/\.py/' | sed 's/^/test_/')
function test {
  python="$1"
  for f in /io/unittest/python/*.py; do
    if ! echo "$SKIP_TESTS" | grep "$(basename "$f")" > /dev/null; then
      printf "\nTesting %s\n" "$f"
      "$python" "$f"
      printf "Ok\n"
    fi
  done
  printf "\n"
}

## Install dependencies
yum -y install eigen3-devel

# Build wheels for python 2.7
pip2 install numpy
python2 setup.py bdist_wheel
LD_LIBRARY_PATH="$PWD/_skbuild/linux-x86_64-2.7/cmake-build:$LD_LIBRARY_PATH" \
  repair_wheel "dist/$(ls -Art dist/ | tail -n 1)"
rm -rf _skbuild

# Build wheels for python 3
for PYBIN in /opt/python/*/bin; do
  VERSION=$(find "$PYBIN" -name 'python[0-9]\.[0-9]' -printf "%f\n" | grep -Eo '[0-9].[0-9]')
  "$PYBIN/pip" install numpy
  "$PYBIN/python" setup.py bdist_wheel

  # Bundle external shared libraries into the wheels
  LD_LIBRARY_PATH="$PWD/_skbuild/linux-x86_64-$VERSION/cmake-build:$LD_LIBRARY_PATH" \
    repair_wheel "dist/$(ls -Art dist/ | tail -n 1)"
  rm -rf _skbuild
done


for whl in wheelhouse/*.whl; do
  wheel unpack "$whl"

  # Put the libs inside the package directory so the relative path to the libs is always the same
  mv eigenpy-2.4.3/eigenpy.libs eigenpy-2.4.3/eigenpy-2.4.3.data/data/lib/python*/site-packages/eigenpy/

  # Repair rpath
  patchelf --set-rpath '$ORIGIN/eigenpy.libs' eigenpy-2.4.3/eigenpy-2.4.3.data/data/lib/python*/site-packages/eigenpy/eigenpy*.so
  patchelf --set-rpath '$ORIGIN' eigenpy-2.4.3/eigenpy-2.4.3.data/data/lib/python*/site-packages/eigenpy/eigenpy.libs/libeigenpy*.so

  # Remove libraries that are present twice
  rm -rf eigenpy-2.4.3/eigenpy-2.4.3.data/data/lib64/libeigenpy.

  wheel pack eigenpy-2.4.3 -d wheelhouse
  rm -rf eigenpy-2.4.3/
done

# Install packages and test
pip2 install eigenpy --no-index --find-links=/io/wheelhouse/
(cd "$HOME"; test python2)

for PYBIN in /opt/python/*/bin; do
    "$PYBIN/pip" install eigenpy --no-index --find-links=/io/wheelhouse/
    (cd "$HOME"; test "$PYBIN/python")
done

rm -rf eigenpy.egg-info/ dist/

ls wheelhouse/
