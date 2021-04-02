# Run a graphical server in a docker and access it from your webbrowser

```bash
docker build -t vnc .
docker run --rm -it -p 6080:6080 vnc
```

You should see:
```
Navigate to this URL:

    http://localhost:6080/vnc.html?host=localhost&port=6080

Press Ctrl-C to exit
```

Open this URL, and then click "Connect".

## For ferrum:

```bash
docker build --add-host "archives.basestation:10.68.1.1" --build-arg=IMAGE=gitlab.laas.fr:4567/gepetto/buildfarm/robotpkg:ferrum -t vnc .
docker run --add-host "archives.basestation:10.68.1.1" --rm -it -p 6080:6080 vnc
```
