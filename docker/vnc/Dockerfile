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
 && chsh -s /bin/bash user \
 && echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER user
ADD --chown=user docker-vnc /usr/local/bin
CMD docker-vnc

USER root

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda.sh \
 && bash /miniconda.sh -b -u -p /opt/miniconda3 \
 && rm /miniconda.sh

RUN mkdir /wan24
RUN chown user /wan24
USER user

RUN /opt/miniconda3/bin/conda config --add channels conda-forge
RUN /opt/miniconda3/bin/conda create -yp /wan24 python=3.10
RUN /opt/miniconda3/bin/conda install -yp /wan24 \
    agm-ws-2023::proxddp \
    agm-ws-2023::proxnlp \
    agm-ws-2023::crocoddyl \
    agm-ws-2023::example-robot-data \
    agm-ws-2023::pinocchio \
    agm-ws-2023::hpp-fcl
