#!/opt/_internal/tools/bin/python
"""
Patch auditwheel whitelist.
Folks at pypa won't allow that in their codebase, as it's ugly, but they don't forbid us to do so:
https://github.com/pypa/auditwheel/issues/76
"""

import sys
import json
from pathlib import Path

USER_PACKAGES = Path(sys.argv[-1])
POLICY = Path('/opt/_internal/tools/lib/python3.7/site-packages/auditwheel/policy/policy.json')

with POLICY.open() as f:
    POLICIES = json.load(f)

deps = []
for dep in USER_PACKAGES.glob('*.libs'):
    deps.append(dep.name)
    for lib in dep.glob('*.so*'):
        POLICIES[-1]["lib_whitelist"].append(lib.name)

with POLICY.open('w') as f:
    json.dump(POLICIES, f)

print(''.join(f':$ORIGIN/../{dep}' for dep in deps))
