#!/opt/_internal/tools/bin/python
"""
Patch auditwheel whitelist: allow reuse of shared objects from our other wheels, 
and generate a string for a RPATH update.

Folks at pypa won't allow that in their codebase, as it's ugly, but they don't forbid us to do so:
https://github.com/pypa/auditwheel/issues/76
"""

import sys
import json
from pathlib import Path

import auditwheel

POLICY = Path(auditwheel.__file__).parent / "policy/policy.json"

with POLICY.open() as f:
    policies = json.load(f)

deps = []
for dep in Path(sys.argv[-1]).glob("*.libs"):
    deps.append(dep.name)
    for lib in dep.glob("*.so*"):
        policies[-1]["lib_whitelist"].append(lib.name)

with POLICY.open("w") as f:
    json.dump(policies, f)

print("".join(f":$ORIGIN/../{dep}" for dep in deps))
