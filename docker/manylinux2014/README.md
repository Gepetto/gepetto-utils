## Build manylinux2014 wheels

This is set of scripts to help build manylinux2014 wheels, the wheels are built for
python 2.7, 3.5, 3.6, 3.7 and 3.8.

To build the wheels :
```
docker build . -t manylinux
docker run -it manylinux -v `pwd`/config:/config -v `pwd`/wheelhouse:/wheelhouse /scripts/build.sh
```

All the wheels can be found in `wheelhouse/`.
