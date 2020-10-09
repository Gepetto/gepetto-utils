#!/bin/bash -eux

export LD_LIBRARY_PATH=/opt/openrobots/lib:$LD_LIBRARY_PATH

TARGET=${1:-eigenpy}
VERSION="$(grep version "/io/config/$TARGET/setup.py" | head -1 | cut -d'"' -f2)"
TARVER="$TARGET-$VERSION"
PACKAGE="$TARGET"
[ "$TARGET" = "hpp-fcl" ] && PACKAGE=hppfcl

for PYBIN in /opt/python/*/bin; do
  PYVERSION=$(find "$PYBIN" -type f -name 'python*.*' | head -1 | grep -Eo "[0-9]\.[0-9]")
  export CMAKE_PREFIX_PATH="$(find / -path "*$PYVERSION*" -type d -name cmake | tr '\n' ':')/opt/openrobots"


  # Build wheels
  "$PYBIN/python" setup.py bdist_wheel -j"$(nproc)" -DBUILD_TESTING=OFF -DINSTALL_DOCUMENTATION=OFF \
      -DCMAKE_INSTALL_LIBDIR=lib -DPYTHON_STANDARD_LAYOUT=ON -DENFORCE_MINIMAL_CXX_STANDARD=ON

  # Bundle external shared libraries into the wheels
  MAIN_LIB_DIR="$PWD/_skbuild/linux-x86_64-$PYVERSION/cmake-install/lib"
  OTHER_LIB_DIRS=$(find / -path "*$PYVERSION*.libs/*" -name *.so | xargs dirname | tr '\n' ':')
  WHEEL_NAME=$(ls -Art dist/ | tail -n 1)

  # Repair it
  LD_LIBRARY_PATH="$MAIN_LIB_DIR:$OTHER_LIB_DIRS$LD_LIBRARY_PATH" \
    auditwheel repair "dist/$WHEEL_NAME" --plat "$PLAT" -w /io/wheelhouse/
  rm -rf _skbuild dist

  # Extract it to move the libs
  WHEEL_DIR="${TARGET/-/_}-$VERSION"
  WHEEL="$(find /io/wheelhouse/ -name "$WHEEL_DIR-cp${PYVERSION/.}*-manylinux2014*.whl")"
  wheel unpack "$WHEEL"
  PACKAGE_DIR="$WHEEL_DIR/$WHEEL_DIR.data/data/lib/python$PYVERSION/site-packages/$PACKAGE"
  MAIN_LIB="$(find $PACKAGE_DIR -name '*.so')"

  # Put the libs inside the package directory so the relative path to the libs is always the same
  mv "$WHEEL_DIR/${TARGET/-/_}.libs" "$PACKAGE_DIR"/
  LIB_DIR="$PACKAGE_DIR/${TARGET/-/_}.libs" # Reassign value because it has changed

  # Change the rpath of the main library so it can find its dependencies
  patchelf --set-rpath "\$ORIGIN/${TARGET/-/_}.libs" "$MAIN_LIB"

  # Set the rpath of the other shared libraries to LIB_DIR so they can find needed libraries in this directory
  for lib in "$LIB_DIR"/*; do
    patchelf --set-rpath '$ORIGIN' "$lib"
  done

  wheel pack "$WHEEL_DIR" -d /io/wheelhouse

  # Install packages and test
  "$PYBIN/pip" install "$TARGET" --no-index --find-links=/io/wheelhouse/
  (cd "$HOME"; "$PYBIN/python" "/io/config/$TARGET/test.py") || touch "/io/wheelhouse/$PYVERSION-$TARGET"

  # Fix generated .cmake files (need to be done after installing the wheels so we know where the shared libraries are installed)
  MAIN_LIB=$(find / ! -path "*$WHEEL_DIR*" -path "*$PYVERSION*${TARGET/-/_}.libs/*" -name "*$TARGET*.so*")
  MAIN_LIB_NAME=$(basename "$MAIN_LIB") # libeigenpy-[hash].so
  MAIN_LIB_NAME_NO_HASH=$(echo $MAIN_LIB_NAME | sed 's/-[[:xdigit:]]\{8\}//') # libeigenpy.so

  # .cmake files should not have references to _skbuild, this is only a temporary fix to be able to build hpp-fcl
  for file in $WHEEL_DIR/$WHEEL_DIR.data/data/lib/cmake/$TARGET/*.cmake
  do
    sed -i "s:/src/_skbuild/linux-x86_64-.*/cmake-install/lib/\(.*\)\.so:\${_IMPORT_PREFIX}/lib/python$PYVERSION/site-packages/$TARGET/$TARGET.libs/\1.so:"  "$file" || true  # TODO HERERERERERERE
    sed -i "s:$MAIN_LIB_NAME_NO_HASH:$MAIN_LIB_NAME:" "$file" || true
    sed -i 's:/src/_skbuild/linux-x86_64-.*/cmake-install/include:${_IMPORT_PREFIX}/include:' "$file" || true
    sed -i 's:/src/_skbuild/linux-x86_64-.*/cmake-install/lib:${_IMPORT_PREFIX}/lib:' "$file" || true
  done

  wheel pack "$WHEEL_DIR" -d /io/wheelhouse
  rm -rf "${WHEEL_DIR:?}"/
done

rm -rf "$TARGET".egg-info/ dist/

mkdir -p /io/dist
mv /io/wheelhouse/* /io/dist/
