# manylinux2014 wheels

This is set of scripts to help build manylinux2014 wheels, the wheels are built for
python 2.7, 3.5, 3.6, 3.7 and 3.8.


## Config

In the `config/config` file, set the variables for your project.

The `config/packages` file need to be edited with the packages needed to build the 
wheels, they need to be specified one per line and will be installed with `yum`.

You can also edit `scripts/pre_builds.sh` if needed, it will be run before building the wheels.


## Build the wheels

To build the wheels run:
```
docker build . -t manylinux
docker run -it -v `pwd`:/work manylinux /work/scripts/setup.sh
```
Then you need to verify that the generated `setup.py` is as you want,
and run `./build_wheels.sh`.

When the build is finished, you can exit docker. All the wheels can be found in `wheelhouse/`.


## Upload the wheels on PyPi
```
twine upload wheelhouse/*
```

## Examples

### eigenpy 2.4.3:

`config/config`:
```
PACKAGE_NAME=eigenpy
TARGET_NAME=eigenpy
VERSION=2.4.3
GIT_URL=https://github.com/stack-of-tasks/eigenpy.git
INSTALL_REQUIRES='["numpy"]'
NPROC=8
```

`config/packages`:
```
eigen3-devel
```

### hppfcl 1.5.1:
`config/config`:
```
PACKAGE_NAME=hppfcl
TARGET_NAME=hppfcl
VERSION=1.5.1
GIT_URL=https://github.com/humanoid-path-planner/hpp-fcl.git
INSTALL_REQUIRES='["numpy"]'
NPROC=8
```

`config/packages`:
```
eigen3-devel
assimp-devel
poly2tri-devel
minizip-devel
irrXML-devel
zlib-devel
```

`script/pre_build.sh`:
```
#!/bin/bash -eux

source "/work/config/config"

for PYBIN in /opt/python/*/bin; do
  "$PYBIN"/pip install numpy
  "$PYBIN"/pip install -i https://test.pypi.org/simple/ eigenpy==2.4.2
done

# TODO: eigenpyTargets-release.cmake has the wrong path to libeigenpy
sed -i 's:IMPORTED_LOCATION_RELEASE "":IMPORTED_LOCATION_RELEASE "/usr/lib/python2.7/site-packages/eigenpy/eigenpy.libs/libeigenpy-453555c1.so":' /usr/lib/cmake/eigenpy/eigenpyTargets-release.cmake
sed -i 's:libeigenpy.so:libeigenpy-453555c1.so:' /usr/lib/cmake/eigenpy/eigenpyTargets-release.cmake

# TODO: the files in /opt/_internal/cpython-*/lib/cmake/eigenpy/eigenpyTargets-release.cmake need to be modified
# TODO: but even then cmake need to be searching in the right directory (with the right python version) to find these files

git clone -j"$NPROC" git://github.com/OctoMap/octomap.git
cd octomap/
mkdir build && cd build
cmake ..
make -j"$NPROC" install
cd /io
rm -rf octomap
```

To build : `LD_LIBRARY_PATH=/usr/lib/python2.7/site-packages/eigenpy/eigenpy.libs:$LD_LIBRARY_PATH ./build_wheels.sh`

Only the python 2.7 wheels are working for now, to test the wheels make sure `libgl1-mesa-dev` is installed.
