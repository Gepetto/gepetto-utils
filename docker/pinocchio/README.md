# Pinocchio Dockerfile

If the buildfarm doesn't work in your case, you could use this.

# Build images

```
docker build -t gepetto/utils:pinocchio-18.04 .
docker build -t gepetto/utils:pinocchio-16.04 --build-arg UBUNTU=xenial .
docker build -t gepetto/utils:pinocchio-14.04 --build-arg UBUNTU=trusty .
```

# Push images

```
docker push gepetto/utils:pinocchio-18.04
docker push gepetto/utils:pinocchio-16.04
docker push gepetto/utils:pinocchio-14.04
```

# Pull an image

```
docker pull gepetto/utils:pinocchio-18.04
docker pull gepetto/utils:pinocchio-16.04
docker pull gepetto/utils:pinocchio-14.04
```

# Run test

```
docker run --rm -it gepetto/utils:pinocchio-18.04
docker run --rm -it gepetto/utils:pinocchio-16.04
docker run --rm -it gepetto/utils:pinocchio-14.04
```

# Enter in the image

```
docker run --rm -it gepetto/utils:pinocchio-18.04 bash
docker run --rm -it gepetto/utils:pinocchio-16.04 bash
docker run --rm -it gepetto/utils:pinocchio-14.04 bash
```
