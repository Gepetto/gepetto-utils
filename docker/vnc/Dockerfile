ARG IMAGE=ubuntu:20.04
FROM $IMAGE

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
    sudo \
 && rm -rf /var/lib/apt/lists/*

EXPOSE 5901

RUN useradd -m user \
 && echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
 && chmod 777 /usr/share/novnc/utils

USER user
ADD docker-vnc /usr/local/bin
CMD docker-vnc
