#!/bin/bash -eux

export LD_LIBRARY_PATH=/opt/openrobots/lib:$LD_LIBRARY_PATH

TARGET=${1:-eigenpy}

function repair_wheel {
  wheel="$1"
  if ! auditwheel show "$wheel"; then
    echo "Skipping non-platform wheel $wheel"
  else
    auditwheel repair "$wheel" --plat "$PLAT" -w /io/wheelhouse/
  fi
}

source "/io/config/$TARGET/config"

# Build wheels
for PYBIN in /opt/python/*/bin; do
  [ -n "$INSTALL_REQUIRES" ] && "$PYBIN/pip" install "$(echo "$INSTALL_REQUIRES" | sed -E 's/"|\[|\]|,//g')"

  PYVERSION=$(find "$PYBIN" -type f -name 'python*.*' | head -1 | grep -Eo "[0-9]\.[0-9]")
  export CMAKE_PREFIX_PATH="$(find / -path "*$PYVERSION*" -type d -name cmake | tr '\n' ':')/opt/openrobots"

  "$PYBIN/python" setup.py bdist_wheel -j"$NPROC" -DBUILD_TESTING=OFF -DINSTALL_DOCUMENTATION=OFF \
      -DCMAKE_INSTALL_LIBDIR=lib -DPYTHON_STANDARD_LAYOUT=ON -DENFORCE_MINIMAL_CXX_STANDARD=ON
  # Bundle external shared libraries into the wheels
  MAIN_LIB_DIR="$PWD/_skbuild/linux-x86_64-$PYVERSION/cmake-install/lib"
  OTHER_LIB_DIRS=$(find / -path "*$PYVERSION*.libs/*" -name *.so | xargs dirname | tr '\n' ':')
  WHEEL_NAME=$(ls -Art dist/ | tail -n 1)

  LD_LIBRARY_PATH="$MAIN_LIB_DIR:$OTHER_LIB_DIRS$LD_LIBRARY_PATH" \
    auditwheel repair "dist/$WHEEL_NAME" --plat "$PLAT" -w /io/wheelhouse/
    #repair_wheel "dist/$WHEEL_NAME"
  rm -rf _skbuild
done

for whl in /io/wheelhouse/*.whl; do
  wheel unpack "$whl"

  MAIN_LIB=$(find . -type f ! -path '*.libs/*' -name '*.so' | grep 'lib/python' | head -1)
  LIB_DIR=$(find . -type d -name '*.libs')
  PACKAGE_DIR=$(dirname "$MAIN_LIB")
  WHEEL_DIR=$(find . -name '*.so' | head -1 | cut -d'/' -f2)

  # Put the libs inside the package directory so the relative path to the libs is always the same
  mv "$LIB_DIR" "$PACKAGE_DIR"/
  LIB_DIR=$(find . -type d -name '*.libs') # Reassign value because it has changed

  # Change the rpath of the main library so it can find its dependencies
  patchelf --set-rpath "\$ORIGIN/$(basename "$LIB_DIR")" "$MAIN_LIB"

  # Set the rpath of the other shared libraries to LIB_DIR so they can find needed libraries in this directory
  for lib in "$LIB_DIR"/*; do
    patchelf --set-rpath '$ORIGIN' "$lib"
  done

  wheel pack "$WHEEL_DIR" -d /io/wheelhouse
  rm -rf "${WHEEL_DIR:?}"/
done

# Install packages and test
for PYBIN in /opt/python/*/bin; do
    "$PYBIN/pip" install "$PACKAGE_NAME" --no-index --find-links=/io/wheelhouse/
    (cd "$HOME"; "$PYBIN/python" "/io/config/$TARGET/test.py")
done

# TODO: Fix generated .cmake files (need to be done after installing the wheels so we know where the shared libraries are installed)
for whl in /io/wheelhouse/*.whl; do
  wheel unpack "$whl"

  WHEEL_DIR=$(find . -name *.so | head -1 | cut -d'/' -f2)
  PYVERSION=$(find "$WHEEL_DIR" -type d -name 'python*' | grep 'lib/python' | tail -c4)
  MAIN_LIB=$(find / ! -path "*$WHEEL_DIR*" -path "*$PYVERSION*$PACKAGE_NAME*.libs/*" -name "*$PACKAGE_NAME*.so*")
  MAIN_LIB_NAME=$(basename "$MAIN_LIB") # libeigenpy-[hash].so
  MAIN_LIB_NAME_NO_HASH=$(echo $MAIN_LIB_NAME | sed 's/-.*\.so/\.so/') # libeigenpy.so

  #TODO: .cmake files should not have references to _skbuild, this is only a temporary fix to be able to build hpp-fcl
  find "$WHEEL_DIR" -name '*.cmake' | while read -r file; do
    sed -i 's:/src/_skbuild/linux-x86_64-.*/cmake-install/include:/usr/local/include:' "$file" || true
    sed -i "s:/src/_skbuild/linux-x86_64-.*/cmake-install/lib/.*\.so:$MAIN_LIB:" "$file" || true
    sed -i "s:$MAIN_LIB_NAME_NO_HASH:$MAIN_LIB_NAME:" "$file" || true
    sed -i 's:/src/_skbuild/linux-x86_64-.*/cmake-install/lib:/usr/local/lib:' "$file" || true
  done

  wheel pack "$WHEEL_DIR" -d /io/wheelhouse
  rm -rf "${WHEEL_DIR:?}"/
done

rm -rf "$PACKAGE_NAME".egg-info/ dist/

mkdir -p /io/dist
mv /io/wheelhouse/* /io/dist/
