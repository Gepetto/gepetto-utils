# Pinocchio Dockerfile

If the buildfarm doesn't work in your case, you could use this.

# Build images

```
docker build -t gepetto/utils:pinocchio-18.04 .
docker build -t gepetto/utils:pinocchio-16.04 --build-arg UBUNTU=xenial .
docker build -t gepetto/utils:pinocchio-14.04 --build-arg UBUNTU=trusty .
docker build -t gepetto/utils:pinocchio-fedora28 -f Dockerfile.fedora .
docker build -t gepetto/utils:pinocchio-fedora27 -f Dockerfile.fedora --build-arg FEDORA=27 .
```

# Push images

```
docker push gepetto/utils:pinocchio-18.04
docker push gepetto/utils:pinocchio-16.04
docker push gepetto/utils:pinocchio-14.04
docker push gepetto/utils:pinocchio-fedora28
docker push gepetto/utils:pinocchio-fedora27
```

# Pull an image

```
docker pull gepetto/utils:pinocchio-18.04
docker pull gepetto/utils:pinocchio-16.04
docker pull gepetto/utils:pinocchio-14.04
docker pull gepetto/utils:pinocchio-fedora28
docker pull gepetto/utils:pinocchio-fedora27
```

# Run test

```
docker run --rm -it gepetto/utils:pinocchio-18.04
docker run --rm -it gepetto/utils:pinocchio-16.04
docker run --rm -it gepetto/utils:pinocchio-14.04
docker run --rm -it gepetto/utils:pinocchio-fedora28
docker run --rm -it gepetto/utils:pinocchio-fedora27
```

# Enter in the image

```
docker run --rm -it gepetto/utils:pinocchio-18.04 bash
docker run --rm -it gepetto/utils:pinocchio-16.04 bash
docker run --rm -it gepetto/utils:pinocchio-14.04 bash
docker run --rm -it gepetto/utils:pinocchio-fedora28 bash
docker run --rm -it gepetto/utils:pinocchio-fedora27 bash
```
