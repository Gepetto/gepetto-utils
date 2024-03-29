#!/usr/bin/env python3
"""Utils to manage Gepetto computers"""

from argparse import ArgumentParser
from datetime import date

import pandas as pd
from ldap3 import Connection
from tabulate import tabulate

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
FILTERS = {
    "laas-mach-group": "gepetto",
    "laas-mach-type": "PC",
}


def short(attr: str) -> str:
    """Use shorter versions of LDAP attributes for CLI & display."""
    return attr.replace("laas-", "").replace("mach-", "").replace("Number", "")


def parse(k, v):
    """Parse ldap value."""
    if not v:
        return ""
    v = v[0]
    if "date" in k:
        d, m, y = (int(i) for i in v.split("/"))
        v = date(y, m, d)
    return v


def filter(**filters) -> str:
    """format some filters for LDAP query."""
    return "".join(f"({k}={v})" for k, v in filters.items())


def machines_ldap(utilisateur="", responsable="", room="", **kwargs):
    """Get a dict of Gepettists machines from LDAP."""
    filters = FILTERS
    if utilisateur:
        filters["laas-mach-utilisateur"] = utilisateur
    if responsable:
        filters["laas-mach-responsable"] = responsable
    if room:
        filters["roomNumber"] = room

    conn = Connection("ldap.laas.fr", auto_bind=True)
    conn.search(
        "ou=machines,dc=laas,dc=fr",
        f"(&{filter(**filters)})",
        attributes=ATTRIBUTES,
    )

    return {
        str(entry.cn): {
            short(k): parse(k, v) for k, v in entry.entry_attributes_as_dict.items()
        }
        for entry in conn.entries
    }


def display(data, sort_by="datePeremption"):
    """Pandas & Tabulate magic to display data."""
    df = pd.DataFrame(data).T.sort_values(by=sort_by)
    print(tabulate(df.drop("cn", axis=1), headers="keys"))


def get_parser() -> ArgumentParser:
    """Configure argparse."""
    parser = ArgumentParser(description=__doc__)

    # Filtering
    parser.add_argument("-u", "--utilisateur")
    parser.add_argument("-r", "--responsable")
    parser.add_argument("-R", "--room")

    # Sorting
    parser.add_argument(
        "-s",
        "--sort_by",
        choices=[short(a) for a in ATTRIBUTES],
        default="datePeremption",
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    data = machines_ldap(**vars(args))
    display(data, args.sort_by)
