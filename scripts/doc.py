#!/usr/bin/env python3

import os
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import requests

DOC = Path('/net/cetus/data/gepetto/Doc')
GITLAB = 'https://gepgitlab.laas.fr'
RAINBOARD = 'http://rainboard.laas.fr'
VERSION = '16.04'


if __name__ == '__main__':
    for project, namespace, branch in requests.get(f'{RAINBOARD}/doc').json()['ret']:
        r = requests.get(f'{GITLAB}/{namespace}/{project}/-/jobs/artifacts/{branch}/download',
                         {'job': f'robotpkg-{project}-{VERSION}'}, stream=True)
        try:
            z = ZipFile(BytesIO(r.content))
            path = DOC / namespace / project / branch
            path.mkdir(parents=True, exist_ok=True)
            z.extractall(str(path))
        except:
            continue
