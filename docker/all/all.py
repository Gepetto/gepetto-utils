#!/usr/bin/env python3
"""
Build all Dockerfiles and check the build result
"""

import concurrent.futures
from subprocess import DEVNULL, CalledProcessError, check_call, check_output

DISTRIBUTIONS = '16.04 18.04 20.04 fedora28 fedora31 archlinux stretch buster centos7'.split()


def build(args):
    """Build a dockerfile."""
    dist, python = args
    tag = f'all/{dist}/py{python}'
    args = {'DIST': dist, 'RPKG': 'robotpkg-py3' if python == 3 else 'robotpkg'}
    args = ' '.join(f'--build-arg {key}={value}' for key, value in args.items())
    try:
        check_call(f'docker build {args} -t {tag} .'.split(), stdout=DEVNULL, stderr=DEVNULL)
    except CalledProcessError:
        return tag, 'build failed'
    try:
        return tag, check_output(f'docker run --rm -it {tag}'.split(), stderr=DEVNULL, universal_newlines=True).strip()
    except CalledProcessError:
        return tag, 'run failed'


if __name__ == '__main__':
    build_args = ((dist, python) for dist in DISTRIBUTIONS for python in (2, 3) if (dist, python) != ('20.04', 2))
    with concurrent.futures.ProcessPoolExecutor(2) as executor:
        for tag, result in executor.map(build, build_args):
            print(f'{tag:20}', ' '.join(result.split('\n')), end='\r\n')
