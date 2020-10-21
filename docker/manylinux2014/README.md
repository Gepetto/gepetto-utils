# manylinux2014 wheels

This is set of scripts to help build manylinux2014 wheels, the wheels are built for
python 2.7, 3.5, 3.6, 3.7, 3.8 and 3.9.


## Build the wheels

To build the wheels run:
```
docker build -t manylinux .
docker run -v (pwd -P):/io -v /local/users/ccache/:/root/.ccache -it manylinux /scripts/setup.sh eigenpy
docker run -v (pwd -P):/io -v /local/users/ccache/:/root/.ccache -it manylinux /scripts/setup.sh hpp-fcl
docker run -v (pwd -P):/io -v /local/users/ccache/:/root/.ccache -it manylinux /scripts/setup.sh pinocchio
```

## Test'em

```
docker build -f test.Dockerfile -t manylinux-test .
docker run --rm -it manylinux-test
```

## Upload the wheels on PyPi

```
twine upload --repository testpypi dist/*
```

## Check everything:

```
for pv in 2.7 3.5 3.6 3.7 3.8 3.9
    docker build -f check.Dockerfile --build-arg PYVER=$pv -t gepetto/utils:wheel-$pv .
    docker push gepetto/utils:wheel-$pv
end
```


## TODO

- use robotpkg to build, instead of downloading the sources: could build all non-python stuff in the docker image
- pyproject.toml in skbuild doc
- lib/pythonX.Y/site-packages/foo.cpython\*.so links to libfoo.so and has RPATH: $ORIGIN/../../../foo.libs
  foo.libs/libfoo.so RPATH: $ORIGIN:$ORIGIN/../bar.libs:$ORIGIN/../baz.libs

  ```cmake
  set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
  set(CMAKE_INSTALL_RPATH "\$ORIGIN;\$ORIGIN/../bar.libs;\$ORIGIN/../baz.libs")
  set_target_properties(foo_pywrap POPERTIES INSTALL_RPATH "\$ORIGIN/../../../foo.libs")
  ```
