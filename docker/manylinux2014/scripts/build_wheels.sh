#!/bin/bash -eux

TARGET=${1:-eigenpy}
PYVER=${2:-3.9}

export CMAKE_PREFIX_PATH="~/.local:/opt/openrobots"
PACKAGE="${TARGET//-/_}"
VERSION="$(cat .version)"
TARVER="$TARGET-$VERSION"
WHEEL_DIR="$PACKAGE-$VERSION"
PYBIN="$(find /opt/python -name "cp${PYVER/.}*")/bin"
INSTALLED_PREFIX="$PWD/_skbuild/linux-x86_64-$PYVER/cmake-install"
USER_SITE="$("$PYBIN/python" -c 'import site; print(site.USER_SITE)')"
SITE_PACKAGES="$("$PYBIN/python" -c "import site; print(site.USER_SITE.replace(site.USER_BASE + '/', ''))")"
LIB_DIR="$PACKAGE.libs"
[ "$PACKAGE" = "hpp_fcl" ] && PACKAGE=hppfcl
PACKAGE_DIR="$WHEEL_DIR/$WHEEL_DIR.data/data/$SITE_PACKAGES/$PACKAGE"

# Install dependencies
"$PYBIN/pip" install --user --find-links=/io/dist/ \
    $(grep install_requires setup.py | sed "s/.*\['//;s/'\].*//;s/,//")

if grep -q skbuild setup.py
then
    # Build binary wheel
    "$PYBIN/python" setup.py bdist_wheel -j"$(nproc)" -DBUILD_TESTING=OFF -DINSTALL_DOCUMENTATION=OFF \
        -DCMAKE_INSTALL_LIBDIR=lib -DPYTHON_STANDARD_LAYOUT=ON -DENFORCE_MINIMAL_CXX_STANDARD=ON

    # Bundle external shared libraries into the wheels
    OTHER_LIB_DIRS=$(find "$USER_SITE" -name '*.libs' | tr '\n' ':')

    # don't bundle ones already in another wheel
    # that's against pypa recomendations, but should work
    WHITELISTED="$(/scripts/patch_whitelist.py "$USER_SITE")"

    # Repair it
    LD_LIBRARY_PATH="$INSTALLED_PREFIX/lib:$OTHER_LIB_DIRS/opt/openrobots/lib:$LD_LIBRARY_PATH" \
        auditwheel repair dist/*.whl --plat "$PLAT" -w /io/wheelhouse/
else
    # Build pure wheel
    cmake -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_INSTALL_PREFIX=. .
    make install
    python setup.py bdist_wheel --universal
    mkdir -p /io/wheelhouse
    mv dist/*.whl /io/wheelhouse
fi

# Clean build
rm -rf _skbuild dist inst

# Extract it
wheel unpack /io/wheelhouse/*.whl

if grep -q skbuild setup.py
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
mv /io/wheelhouse/*.whl /io/dist
