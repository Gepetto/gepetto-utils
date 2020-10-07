#!/usr/bin/env python3
"""
Build all Dockerfiles and check the build result
"""

import asyncio
import sys
from asyncio.subprocess import DEVNULL, PIPE

DISTRIBUTIONS = '16.04 18.04 20.04 fedora28 fedora31 archlinux stretch buster centos7'.split()


async def build_run(dist, verbose=False, parallel=1):
    """Build and run a dockerfile."""
    cmd = f'docker build --build-arg DIST={dist} --build-arg PARALLEL={parallel} -t all/{dist} .'
    if verbose:
        print(f'+ {cmd}\r')
    proc = await asyncio.create_subprocess_exec(*cmd.split(), stdout=DEVNULL, stderr=DEVNULL)
    await proc.wait()
    if proc.returncode != 0:
        print(f'{dist:10} build failed\r')
        return
    cmd = f'docker run --rm -it all/{dist}'
    if verbose:
        print(f'+ {cmd}\r')
    proc = await asyncio.create_subprocess_exec(*cmd.split(), stdout=PIPE, stderr=DEVNULL)
    stdout, _ = await proc.communicate()
    stdout = stdout.decode().replace('\r\n', ' ')
    if proc.returncode == 0:
        print(f'{dist:10} {stdout}\r')
    else:
        print(f'{dist:10} run failed\r')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if len(sys.argv) > 1:
        loop.run_until_complete(build_run(sys.argv[1], verbose=True, parallel=8))
    else:
        loop.run_until_complete(asyncio.gather(*(build_run(dist) for dist in DISTRIBUTIONS)))
    loop.close()
