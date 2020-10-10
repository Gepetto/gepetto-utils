#!/bin/bash -eux

TARGET=${1:-eigenpy}
PYVER=${2:-3.9}

export LD_LIBRARY_PATH=/opt/openrobots/lib:$LD_LIBRARY_PATH

VERSION="$(grep version "/io/config/$TARGET/setup.py" | head -1 | cut -d'"' -f2)"
TARVER="$TARGET-$VERSION"
PACKAGE="$TARGET"
[ "$TARGET" = "hpp-fcl" ] && PACKAGE=hppfcl
PYBIN="$(find /opt/python -name "cp${PYVER/.}*")/bin"

# Install dependencies
"$PYBIN/pip" install --user --find-links=/io/dist/ \
    $(grep install_requires "/io/config/$TARGET/setup.py" | sed "s/.*\['//;s/'\].*//;s/,//")

export CMAKE_PREFIX_PATH="~/.local:/opt/openrobots"

# Build wheels
"$PYBIN/python" setup.py bdist_wheel -j"$(nproc)" -DBUILD_TESTING=OFF -DINSTALL_DOCUMENTATION=OFF \
    -DCMAKE_INSTALL_LIBDIR=lib -DPYTHON_STANDARD_LAYOUT=ON -DENFORCE_MINIMAL_CXX_STANDARD=ON

# Bundle external shared libraries into the wheels
INSTALLED_PREFIX="$PWD/_skbuild/linux-x86_64-$PYVER/cmake-install"
SITE_PACKAGES="lib/python$PYVER/site-packages"
USER_PACKAGES="$HOME/.local/$SITE_PACKAGES"
OTHER_LIB_DIRS=$(find "$USER_PACKAGES" -name '*.libs' | tr '\n' ':')
WHEEL_NAME=$(ls -Art dist/ | tail -n 1)

# don't bundle ones already in another wheel
# that's against pypa recomendations, but should work
WHITELISTED="$(/scripts/patch_whitelist.py "$USER_PACKAGES")"

# Repair it
LD_LIBRARY_PATH="$INSTALLED_PREFIX/lib:$OTHER_LIB_DIRS$LD_LIBRARY_PATH" \
    auditwheel repair "dist/$WHEEL_NAME" --plat "$PLAT" -w /io/wheelhouse/
rm -rf _skbuild dist

# Extract it
WHEEL_DIR="${TARGET/-/_}-$VERSION"
WHEEL="$(find /io/wheelhouse/ -name "$WHEEL_DIR-cp${PYVER/.}*-manylinux2014*.whl")"
wheel unpack "$WHEEL"
PACKAGE_DIR="$WHEEL_DIR/$WHEEL_DIR.data/data/$SITE_PACKAGES/$PACKAGE"

# set the RPATH right for the installed wheel
# ref https://github.com/pypa/auditwheel/issues/257
LIB_DIR="${TARGET/-/_}.libs"
patchelf --set-rpath "\$ORIGIN/../$LIB_DIR$WHITELISTED" "$(find "$PACKAGE_DIR" -name '*.so')"

# Remove duplicated libs
rm -f "$WHEEL_DIR/$WHEEL_DIR.data/data/lib/"lib*so*

# Set the rpath of the other shared libraries in LIB_DIR
for lib in "$WHEEL_DIR/${LIB_DIR}"/*
do patchelf --set-rpath '$ORIGIN' "$lib"
done

# .cmake files should not have references to _skbuild, this is only a temporary fix to be able to build hpp-fcl
MAIN_LIB=$(find "$WHEEL_DIR/$LIB_DIR" -name "lib$TARGET-*.so") # eigenpy-2.5.0/eigenpy.libs/libeigenpy-0c5e8890.so
MAIN_LIB_NAME=$(basename "$MAIN_LIB") # libeigenpy-0c5e8890.so
MAIN_LIB_NAME_NO_HASH=$(echo "$MAIN_LIB_NAME" | sed 's/-[[:xdigit:]]\{8\}//') # libeigenpy.so

for file in $WHEEL_DIR/$WHEEL_DIR.data/data/lib/cmake/$TARGET/*.cmake
do
    sed -i "s:/src/_skbuild/linux-x86_64-.*/cmake-install/lib/\(.*\)\.so:\${_IMPORT_PREFIX}/$SITE_PACKAGES/$LIB_DIR/\1.so:" "$file" || true
    sed -i "s:$MAIN_LIB_NAME_NO_HASH:$MAIN_LIB_NAME:" "$file" || true
    sed -i 's:/src/_skbuild/linux-x86_64-.*/cmake-install/include:${_IMPORT_PREFIX}/include:' "$file" || true
    sed -i 's:/src/_skbuild/linux-x86_64-.*/cmake-install/lib:${_IMPORT_PREFIX}/lib:' "$file" || true
done

# Repack and clean
wheel pack "$WHEEL_DIR" -d /io/wheelhouse
rm -rf "${WHEEL_DIR:?}"/

# Install packages and test
"$PYBIN/pip" install --user "$TARGET" --no-index --find-links=/io/wheelhouse/
(cd "$HOME"; "$PYBIN/python" "/io/config/$TARGET/test.py") || touch "/io/wheelhouse/$PYVER-$TARGET"

rm -rf "$TARGET".egg-info/ dist/

mkdir -p /io/dist
mv /io/wheelhouse/* /io/dist/
