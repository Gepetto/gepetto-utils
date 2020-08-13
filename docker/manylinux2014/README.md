# manylinux2014 wheels

This is set of scripts to help build manylinux2014 wheels, the wheels are built for
python 2.7, 3.5, 3.6, 3.7 and 3.8.

## Config

In the `config/config` file, set the variables for your project.

The `config/packages` file need to be edited with the packages needed to build the 
wheels, they need to be specified one per line and will with `yum`.

#### Example config to build wheels for eigenpy 2.4.3:

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

## Build the wheels

To build the wheels run:
```
docker build . -t manylinux
docker run -it -v `pwd`:/work manylinux /work/scripts/build.sh
```
Then you need to verify that the generated `setup.py` is as you want,
and run `./build_wheels.sh`.

When the build is finished, you can exit docker. All the wheels can be found in `wheelhouse/`.

## Upload the wheels on PyPi
```
twine upload wheelhouse/*
```
