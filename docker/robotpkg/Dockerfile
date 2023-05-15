FROM ubuntu:jammy

ADD http://robotpkg.openrobots.org/packages/debian/robotpkg.asc /etc/apt/keyrings/robotpkg.asc
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/robotpkg.asc] http://robotpkg.openrobots.org/wip/packages/debian/pub jammy robotpkg" /etc/apt/sources.list.d/robotpkg.list
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/robotpkg.asc] http://robotpkg.openrobots.org/packages/debian/pub jammy robotpkg" /etc/apt/sources.list.d/robotpkg.list
