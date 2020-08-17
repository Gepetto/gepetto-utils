#!/usr/bin/env python3
"""
Build all Dockerfiles and check the build result
"""

from multiprocessing import Pool
from pathlib import Path
from subprocess import DEVNULL, CalledProcessError, check_call, check_output


def build(path):
    """Build a dockerfile."""
    path = str(path.parent)
    tag = f'all/{path}'
    try:
        check_call(f'docker build -f {path}/Dockerfile -t {tag} .'.split(), stdout=DEVNULL, stderr=DEVNULL)
    except CalledProcessError:
        return path, 'build failed'
    try:
        return path, check_output(f'docker run --rm -it {tag}'.split(), stderr=DEVNULL).decode().strip()
    except CalledProcessError:
        return path, 'run failed'


if __name__ == '__main__':
    with Pool(12) as p:
        for job, result in p.map(build, Path('.').glob('*/*/Dockerfile')):
            print(f'{job:15}', result, end='\r\n')
