#!/usr/bin/env python3
"""Utils to manage Gepetto computers"""

from argparse import ArgumentParser
from datetime import date

import pandas as pd
from ldap3 import Connection
from tabulate import tabulate

CONN = Connection("ldap.laas.fr", auto_bind=True)
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
    "laas-mach-commentaire",
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


def machines_ldap(utilisateur="", responsable="", room="", machine="", **kwargs):
    """Get a dict of Gepettists machines from LDAP."""
    filters = FILTERS
    if machine:
        filters["cn"] = machine
    if utilisateur:
        filters["laas-mach-utilisateur"] = utilisateur
    if responsable:
        filters["laas-mach-responsable"] = responsable
    if room:
        filters["roomNumber"] = room

    CONN.search(
        "ou=machines,dc=laas,dc=fr",
        f"(&{filter(**filters)})",
        attributes=ATTRIBUTES,
    )

    return {
        str(entry.cn): {
            short(k): parse(k, v) for k, v in entry.entry_attributes_as_dict.items()
        }
        for entry in CONN.entries
    }


def users_ldap():
    """Get a dict of Gepettists with their room and st"""
    CONN.search(
        "ou=users,dc=laas,dc=fr", "(o=gepetto)", attributes=["uid", "st", "roomNumber"]
    )

    return {
        str(entry.uid): {
            short(k): parse(k, v) for k, v in entry.entry_attributes_as_dict.items()
        }
        for entry in CONN.entries
    }


def machines_display(data, sort_by="datePeremption"):
    """Pandas & Tabulate magic to display machines data."""
    df = pd.DataFrame(data).T.sort_values(by=sort_by)
    print(tabulate(df.drop("cn", axis=1), headers="keys"))


def get_parser() -> ArgumentParser:
    """Configure argparse."""
    parser = ArgumentParser(description=__doc__)

    # Filtering
    parser.add_argument("-m", "--machine")
    parser.add_argument("-R", "--responsable")
    parser.add_argument("-u", "--utilisateur")
    parser.add_argument("-r", "--room")

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
    machines_data = machines_ldap(**vars(args))
    if not machines_data:
        print("nothing was found.")
    else:
        machines_display(machines_data, args.sort_by)
        print()
        users_data = users_ldap()
        for k, v in machines_data.items():
            if not v["utilisateur"] or v["utilisateur"] not in users_data:
                print(f"{k}: wrong user {v['utilisateur']}")
                continue
            user = users_data[v["utilisateur"]]
            if user["room"] != v["room"]:
                print(f"{k}: wrong user's room {user['room']} != {v['room']}")
            if user["st"] in ["JAMAIS", "NON-PERTINENT"]:
                continue
            d, m, y = (int(i) for i in user["st"].split("/"))
            st = date(y, m, d)
            if v["datePeremption"] > st:
                print(
                    f"{k}: wrong peremption for {user['uid']}: "
                    f"{v['datePeremption']:%d/%m/%Y} > {st:%d/%m/%Y}"
                )
