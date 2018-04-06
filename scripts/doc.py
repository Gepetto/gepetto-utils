#!/usr/bin/env python3

import os
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import requests

DOC = Path('/net/cetus/data/gepetto/Doc')
GITLAB = 'https://gepgitlab.laas.fr'
VERSION = '16.04'

PR_NS_BR = [
    ('pinocchio', [
        ('gsaurel', [
            'autodeploy-doc',
        ]),
    ]),
]

for project, namespaces in PR_NS_BR:
    for namespace, branches in namespaces:
        for branch in branches:
            path = DOC / namespace / project / branch
            path.mkdir(parents=True, exist_ok=True)
            r = requests.get(f'{GITLAB}/{namespace}/{project}/-/jobs/artifacts/{branch}/download',
                             {'job': f'robotpkg-{project}-{VERSION}'}, stream=True)
            ZipFile(BytesIO(r.content)).extractall(str(path))
