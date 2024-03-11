#!/usr/bin/env python3
"""Utils to manage Gepetto computers"""

from datetime import date

import pandas as pd
from ldap3 import Connection

ATTRIBUTES = [
    "cn",
    "laas-date-install",
    "laas-mach-datePeremption",
    "laas-mach-inventaire",
    "laas-mach-modele",
    "laas-mach-os",
    "laas-mach-responsable",
    # "laas-mach-type",
    "laas-mach-utilisateur",
    "roomNumber",
]


def parse(k, v):
    """Parse ldap value."""
    if not v:
        return ""
    v = v[0]
    if "date" in k:
        d, m, y = (int(i) for i in v.split("/"))
        v = date(y, m, d)
    return v


def machines_ldap():
    """Get a dict of Gepettists machines from LDAP."""
    conn = Connection("ldap.laas.fr", auto_bind=True)
    conn.search(
        "ou=machines,dc=laas,dc=fr",
        "(&(laas-mach-group=gepetto)(laas-mach-type=PC))",
        attributes=ATTRIBUTES,
    )
    df = pd.DataFrame(
        {
            str(entry.cn): {
                k: parse(k, v)
                for k, v in entry.entry_attributes_as_dict.items()
                if k != "cn"
            }
            for entry in conn.entries
        }
    ).T.sort_values(by="laas-mach-datePeremption")
    print(df.to_markdown())
    return df


if __name__ == "__main__":
    df = machines_ldap()
