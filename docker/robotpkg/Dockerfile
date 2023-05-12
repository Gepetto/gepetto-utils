FROM ubuntu:jammy

# Setup Robotpkg apt binary repository
ADD http://robotpkg.openrobots.org/packages/debian/robotpkg.key /
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -qqy --no-install-recommends \
    gnupg2 \
 && gpg --dearmor /robotpkg.key \
 && mv /robotpkg.key.gpg /usr/share/keyrings/robotpkg.gpg \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/robotpkg.gpg] \
          http://robotpkg.openrobots.org/packages/debian/pub jammy robotpkg" \
 >> /etc/apt/sources.list.d/robotpkg.list \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/robotpkg.gpg] \
          http://robotpkg.openrobots.org/wip/packages/debian/pub jammy robotpkg" \
 >> /etc/apt/sources.list.d/robotpkg.list
