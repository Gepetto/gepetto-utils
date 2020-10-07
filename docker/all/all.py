#!/usr/bin/env python3
"""
Build all Dockerfiles and check the build result
"""

import asyncio
from asyncio.subprocess import PIPE, DEVNULL

DISTRIBUTIONS = '16.04 18.04 20.04 fedora28 fedora31 archlinux stretch buster centos7'.split()


async def build_run(dist):
    """Build and run a dockerfile."""
    cmd = f'docker build --build-arg DIST={dist} -t all/{dist} .'.split()
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=DEVNULL, stderr=DEVNULL)
    await proc.wait()
    if proc.returncode != 0:
        print(f'{dist:10} build failed\r')
        return
    cmd = f'docker run --rm -it all/{dist}'.split()
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=DEVNULL)
    stdout, _ = await proc.communicate()
    stdout = stdout.decode().replace('\r\n', ' ')
    if proc.returncode == 0:
        print(f'{dist:10} {stdout}\r')
    else:
        print(f'{dist:10} run failed\r')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*(build_run(dist) for dist in DISTRIBUTIONS)))
    loop.close()
