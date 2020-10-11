#!/bin/bash -eux

TARGET=${1:-eigenpy}
PYVER=${2:-3.9}

export CMAKE_PREFIX_PATH="~/.local:/opt/openrobots"
PACKAGE="${TARGET//-/_}"
VERSION="$(grep version setup.py | head -1 | cut -d'"' -f2)"
TARVER="$TARGET-$VERSION"
WHEEL_DIR="$PACKAGE-$VERSION"
PYBIN="$(find /opt/python -name "cp${PYVER/.}*")/bin"
INSTALLED_PREFIX="$PWD/_skbuild/linux-x86_64-$PYVER/cmake-install"
SITE_PACKAGES="lib/python$PYVER/site-packages"
USER_PACKAGES="$HOME/.local/$SITE_PACKAGES"
WHEEL_NAME="$WHEEL_DIR-cp${PYVER/.}-"
LIB_DIR="$PACKAGE.libs"
[ "$PACKAGE" = "hpp_fcl" ] && PACKAGE=hppfcl
PACKAGE_DIR="$WHEEL_DIR/$WHEEL_DIR.data/data/$SITE_PACKAGES/$PACKAGE"

# Install dependencies
"$PYBIN/pip" install --user --find-links=/io/dist/ \
    $(grep install_requires setup.py | sed "s/.*\['//;s/'\].*//;s/,//")

# Build wheels
"$PYBIN/python" setup.py bdist_wheel -j"$(nproc)" -DBUILD_TESTING=OFF -DINSTALL_DOCUMENTATION=OFF \
    -DCMAKE_INSTALL_LIBDIR=lib -DPYTHON_STANDARD_LAYOUT=ON -DENFORCE_MINIMAL_CXX_STANDARD=ON

BINARY_EXTENSIONS="$(find "$INSTALLED_PREFIX/$SITE_PACKAGES/$PACKAGE" -name '*.so*')" || true
if [ -n "$BINARY_EXTENSIONS" ]
then
    # Bundle external shared libraries into the wheels
    OTHER_LIB_DIRS=$(find "$USER_PACKAGES" -name '*.libs' | tr '\n' ':')

    # don't bundle ones already in another wheel
    # that's against pypa recomendations, but should work
    WHITELISTED="$(/scripts/patch_whitelist.py "$USER_PACKAGES")"

    # Repair it
    LD_LIBRARY_PATH="$INSTALLED_PREFIX/lib:$OTHER_LIB_DIRS/opt/openrobots/lib:$LD_LIBRARY_PATH" \
        auditwheel repair "dist/$WHEEL_NAME"* --plat "$PLAT" -w /io/wheelhouse/
else
    mv dist/"$WHEEL_NAME"*-linux*.whl /io/wheelhouse
fi

# Clean build
rm -rf _skbuild dist

# Extract it
wheel unpack /io/wheelhouse/"$WHEEL_NAME"*linux*.whl

if [ -n "$BINARY_EXTENSIONS" ]
then
    # set the RPATH right for the installed wheel
    # ref https://github.com/pypa/auditwheel/issues/257
    patchelf --set-rpath "\$ORIGIN/../$LIB_DIR$WHITELISTED" "$(find "$PACKAGE_DIR" -name '*.so')"

    # Remove moved libs
    rm -f "$WHEEL_DIR/$WHEEL_DIR.data/data/lib/"lib*so*

    # Set the rpath of the other shared libraries in LIB_DIR
    for lib in "$WHEEL_DIR/${LIB_DIR}"/*
    do patchelf --set-rpath '$ORIGIN' "$lib"
    done

    # fix .cmake files: remove _skbuild references & update lib name with their hash from auditwheel
    MAIN_LIB=$(find "$WHEEL_DIR/$LIB_DIR" -name "lib$TARGET-*.so*") # eigenpy-2.5.0/eigenpy.libs/libeigenpy-0c5e8890.so
    MAIN_LIB_NAME=$(basename "$MAIN_LIB") # libeigenpy-0c5e8890.so
    MAIN_LIB_NAME_NO_HASH=$(echo "$MAIN_LIB_NAME" | sed 's/-[[:xdigit:]]\{8\}//') # libeigenpy.so

    for file in $WHEEL_DIR/$WHEEL_DIR.data/data/lib/cmake/$TARGET/*.cmake
    do
        sed -i "s:$MAIN_LIB_NAME_NO_HASH:$MAIN_LIB_NAME:" "$file" || true
    done
fi

for file in $WHEEL_DIR/$WHEEL_DIR.data/data/lib/cmake/$TARGET/*.cmake
do
    sed -i "s:/src/_skbuild/linux-x86_64-.*/cmake-install/lib/\([^/]*\)\.so:\${_IMPORT_PREFIX}/$SITE_PACKAGES/$LIB_DIR/\1.so:" "$file" || true
    sed -i 's:/src/_skbuild/linux-x86_64-.*/cmake-install/include:${_IMPORT_PREFIX}/include:' "$file" || true
    sed -i 's:/src/_skbuild/linux-x86_64-.*/cmake-install/lib:${_IMPORT_PREFIX}/lib:' "$file" || true
done

# Repack and clean
wheel pack "$WHEEL_DIR" -d /io/wheelhouse
rm -rf "${WHEEL_DIR:?}"/ "$TARGET".egg-info

# Install packages and test
"$PYBIN/pip" install --user "$TARGET" --no-index --find-links=/io/wheelhouse/
(cd "$HOME"; "$PYBIN/python" "/io/config/$TARGET/test.py")

mkdir -p /io/dist
mv /io/wheelhouse/"$WHEEL_NAME"*linux*.whl /io/dist
