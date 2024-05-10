#!/usr/bin/env python3

from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import httpx

DOC = Path("/net/cubitus/projects/Partage_GEPETTO/Doc")
GITLAB = "https://gitlab.laas.fr"
RAINBOARD = "https://rainboard.laas.fr"
INDEX = DOC / "index.html"
HEAD = DOC / "index.head.html"

if __name__ == "__main__":
    with INDEX.open("w") as f, HEAD.open() as head:
        f.write(head.read())

    for project, namespace, branch in sorted(
        httpx.get(f"{RAINBOARD}/doc").json()["ret"]
    ):
        url = f"{GITLAB}/{namespace}/{project}/-/jobs/artifacts/{branch}/download"
        path = DOC / namespace / project / branch
        r = httpx.get(url, {"job": "doc-coverage"}, stream=True)
        try:
            z = ZipFile(BytesIO(r.content))
            path.mkdir(parents=True, exist_ok=True)
            z.extractall(str(path))
        except Exception:
            pass

        if path.exists():
            with INDEX.open("a") as f:
                link = path.relative_to(DOC)
                doxygen, coverage = link / "doxygen-html", link / "coverage"
                print(
                    f"<tr><td>{project}</td><td>{namespace}</td><td>{branch}</td><td>",
                    file=f,
                )
                if (DOC / doxygen).is_dir():
                    print(f"<a href='{doxygen}'>Doc</a>", file=f)
                print("</td><td>", file=f)
                if (DOC / coverage).is_dir():
                    print(f"<a href='{coverage}'>Coverage</a>", file=f)
                print("</td></tr>", file=f)

    with INDEX.open("a") as f:
        print("</table></body></html>", file=f)
