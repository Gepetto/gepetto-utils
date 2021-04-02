ARG IMAGE=ubuntu18.04O
FROM IMAGE

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

EXPOSE 5901

ADD docker-vnc /usr/local/bin
CMD docker-vnc
