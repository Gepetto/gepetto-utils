#!/usr/bin/env python3
"""
Build all Dockerfiles and check the build result
"""

import concurrent.futures
from subprocess import DEVNULL, CalledProcessError, check_call, check_output

DISTRIBUTIONS = '16.04 18.04 20.04 fedora28 fedora31 archlinux stretch buster centos7'.split()


def build(dist):
    """Build a dockerfile."""
    try:
        check_call(f'docker build --build-arg DIST={dist} -t all/{dist} .'.split(), stdout=DEVNULL, stderr=DEVNULL)
    except CalledProcessError:
        return dist, 'build failed'
    try:
        return dist, check_output(f'docker run --rm -it all/{dist}'.split(), stderr=DEVNULL,
                                  universal_newlines=True).strip()
    except CalledProcessError:
        return dist, 'run failed'


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(2) as executor:
        for dist, result in executor.map(build, DISTRIBUTIONS):
            print(f'{dist:10}', ' '.join(result.split('\n')), end='\r\n')
