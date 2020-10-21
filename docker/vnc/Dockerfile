FROM ubuntu:18.04

RUN apt-get update -qqy \
 && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    git \
    mesa-utils \
    net-tools \
    novnc \
    tigervnc-standalone-server \
    tigervnc-xorg-extension \
    terminator \
    x11-apps \
    xfce4 \
 && rm -rf /var/lib/apt/lists/*

ADD docker-vnc /usr/local/bin
CMD docker-vnc
