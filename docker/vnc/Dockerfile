FROM ubuntu:focal

RUN --mount=type=cache,sharing=locked,target=/var/cache/apt --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt-get update -qqy && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    git \
    mesa-utils \
    net-tools \
    novnc \
    sudo \
    tigervnc-standalone-server \
    tigervnc-xorg-extension \
    terminator \
    x11-apps \
    xfce4

EXPOSE 5912

RUN chmod 777 /usr/share/novnc/utils \
 && useradd -m user \
 && sed -i '/user/s/:x:/::/' /etc/passwd \
 && echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER user
ADD --chown=user docker-vnc /usr/local/bin
CMD docker-vnc
