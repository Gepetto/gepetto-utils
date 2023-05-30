FROM ubuntu:jammy

ADD --chmod=644 http://robotpkg.openrobots.org/packages/debian/robotpkg.gpg /robotpkg.gpg
RUN echo "deb [arch=amd64 signed-by=/robotpkg.gpg] http://robotpkg.openrobots.org/wip/packages/debian/pub jammy robotpkg" >> /etc/apt/sources.list.d/robotpkg.list
RUN echo "deb [arch=amd64 signed-by=/robotpkg.gpg] http://robotpkg.openrobots.org/packages/debian/pub jammy robotpkg" >> /etc/apt/sources.list.d/robotpkg.list
