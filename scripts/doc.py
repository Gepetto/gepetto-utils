#!/usr/bin/env python3

import os
from pathlib import Path
from zipfile import BadZipFile, ZipFile
from io import BytesIO
import requests

DOC = Path('/net/pongo/vol/vol_projects/partage_gepetto/Doc')
GITLAB = 'https://gepgitlab.laas.fr'
RAINBOARD = 'http://rainboard.laas.fr'
INDEX = DOC / 'index.html'
HEAD = DOC / 'index.head.html'


if __name__ == '__main__':
    with INDEX.open('w') as f:
        with HEAD.open() as head:
            f.write(head.read())

    for project, namespace, branch in sorted(requests.get(f'{RAINBOARD}/doc').json()['ret']):
        url = f'{GITLAB}/{namespace}/{project}/-/jobs/artifacts/{branch}/download'
        path = DOC / namespace / project / branch
        r = requests.get(url, {'job': 'doc-coverage'}, stream=True)
        try:
            z = ZipFile(BytesIO(r.content))
            path.mkdir(parents=True, exist_ok=True)
            z.extractall(str(path))
        except BadZipFile:
            pass

        if path.exists():
            with INDEX.open('a') as f:
                link = path.relative_to(DOC)
                doxygen, coverage = link / 'doxygen-html', link / 'coverage'
                print(f'<tr><td>{project}</td><td>{namespace}</td><td>{branch}</td><td>', file=f)
                if (DOC / doxygen).is_dir():
                    print(f'<a href="{doxygen}">Doc</a>', file=f)
                print('</td><td>', file=f)
                if (DOC / coverage).is_dir():
                    print(f'<a href="{coverage}">Coverage</a>', file=f)
                print('</td></tr>', file=f)

    with INDEX.open('a') as f:
        print('</table></body></html>', file=f)
