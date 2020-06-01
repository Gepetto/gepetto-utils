#!/usr/bin/env python3

from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import requests

DOC = Path('/net/pongo/vol/vol_projects/partage_gepetto/Doc')
GITLAB = 'https://gitlab.laas.fr'
RAINBOARD = 'http://rainboard.laas.fr'
INDEX = DOC / 'index.html'
HEAD = DOC / 'index.head.html'

if __name__ == '__main__':
    with INDEX.open('w') as f:
        with HEAD.open() as head:
            f.write(head.read())

    for project, namespace, branch in sorted(requests.get('%s/doc' % RAINBOARD).json()['ret']):
        url = '%s/%s/%s/-/jobs/artifacts/%s/download' % (GITLAB, namespace, project, branch)
        path = DOC / namespace / project / branch
        r = requests.get(url, {'job': 'doc-coverage'}, stream=True)
        try:
            z = ZipFile(BytesIO(r.content))
            path.mkdir(parents=True, exist_ok=True)
            z.extractall(str(path))
        except Exception:
            pass

        if path.exists():
            with INDEX.open('a') as f:
                link = path.relative_to(DOC)
                doxygen, coverage = link / 'doxygen-html', link / 'coverage'
                print('<tr><td>%s</td><td>%s</td><td>%s</td><td>' % (project, namespace, branch), file=f)
                if (DOC / doxygen).is_dir():
                    print('<a href="%s">Doc</a>' % doxygen, file=f)
                print('</td><td>', file=f)
                if (DOC / coverage).is_dir():
                    print('<a href="%s">Coverage</a>' % coverage, file=f)
                print('</td></tr>', file=f)

    with INDEX.open('a') as f:
        print('</table></body></html>', file=f)
