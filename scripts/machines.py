#!/usr/bin/env python3
"""Utils to manage Gepetto computers"""

from argparse import ArgumentParser
from datetime import date, datetime
from json import load
from logging import basicConfig, getLogger
from os import environ
from pathlib import Path

import pandas as pd
from ldap3 import Connection
from tabulate import tabulate

TODAY = date.today()
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
    "laas-mach-group": ["gepetto"],
    "laas-mach-type": ["PC"],
    "laas-mach-origineAchat": ["LAAS", "autre"],  # exclude perso
}
ALLOWED_ROOMS = ["A148", "B10", "B12", "B15", "B114"]

logger = getLogger("machines")


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

    def filter_key(k, vs):
        return "(|" + "".join(f"({k}={v})" for v in vs) + ")"

    return "(&" + "".join(filter_key(k, vs) for k, vs in filters.items()) + ")"


def machines_ldap(
    utilisateur="", responsable="", room="", machine="", vlan=False, **kwargs
):
    """Get a dict of Gepettists machines from LDAP."""
    filters = FILTERS
    if machine:
        filters["cn"] = [machine]
    if utilisateur:
        filters["laas-mach-utilisateur"] = [utilisateur]
    if responsable:
        filters["laas-mach-responsable"] = [responsable]
    if room:
        filters["roomNumber"] = [room]

    CONN.search(
        "ou=machines,dc=laas,dc=fr",
        filter(**filters),
        attributes=ATTRIBUTES,
    )

    ret = {
        str(entry.cn): {
            short(k): parse(k, v) for k, v in entry.entry_attributes_as_dict.items()
        }
        for entry in CONN.entries
    }

    inv_to_cn = {
        str(entry["laas-mach-inventaire"]): str(entry.cn) for entry in CONN.entries
    }

    if vlan:
        filters = "".join(f"(cn={k})" for k in ret.keys())
        attributes = ["cn", "laas-vlan", "laas-vlan-name"]
        CONN.search("ou=hosts,dc=laas,dc=fr", f"(|{filters})", attributes=attributes)

        for entry in CONN.entries:
            cn, vlan, name = (str(entry[k]) for k in attributes)
            ret[cn]["vlan"] = f"{vlan}: {name}"

    with Path("data/entree.json").open() as f:
        for k, v in load(f).items():
            ret[inv_to_cn[k]]["date-entree"] = datetime.strptime(v, "%Y-%m-%d").date()

    return ret


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


def machines_display(data, output_format, sort_by="datePeremption"):
    """Pandas & Tabulate magic to display machines data."""
    df = pd.DataFrame(data).T.sort_values(by=sort_by).drop("cn", axis=1)
    match output_format:
        case "csv":
            print(df.to_csv())
        case "df":
            print(pd.DataFrame(data))
        case "dict":
            print(df.to_dict())
        case "json":
            print(df.T.to_json())
        case "table":
            print(tabulate(df, headers="keys"))


def get_parser() -> ArgumentParser:
    """Configure argparse."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-V", "--vlan", action="store_true")

    # Filtering
    parser.add_argument("-m", "--machine")
    parser.add_argument("-R", "--responsable")
    parser.add_argument("-u", "--utilisateur")
    parser.add_argument("-r", "--room")
    parser.add_argument(
        "-f",
        "--output-format",
        default="table",
        choices=["csv", "df", "dict", "json", "table"],
    )

    # Logging

    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=int(environ.get("QUIET", 0)),
        help="decrement verbosity level",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=int(environ.get("VERBOSITY", 0)),
        help="increment verbosity level",
    )

    # Sorting
    parser.add_argument(
        "-s",
        "--sort_by",
        choices=[short(a) for a in ATTRIBUTES] + ["date-entree"],
        default="datePeremption",
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    basicConfig(level=30 - 10 * args.verbose + 10 * args.quiet)
    machines_data = machines_ldap(**vars(args))
    if not machines_data:
        print("nothing was found.")
    else:
        machines_display(machines_data, args.output_format, args.sort_by)
        print()
        users_data = users_ldap()
        for k, v in machines_data.items():
            if not v["utilisateur"] or v["utilisateur"] not in users_data:
                logger.warning(f"{k}: wrong user '{v['utilisateur']}'")
                continue
            user = users_data[v["utilisateur"]]
            if user["room"] != v["room"] and v["room"] not in ALLOWED_ROOMS:
                logger.warning(
                    f"{k}: wrong user's ({user['uid']}) room "
                    f"'{user['room']}' != '{v['room']}'"
                )
            if user["st"] in ["JAMAIS", "NON-PERTINENT"]:
                continue
            d, m, y = (int(i) for i in user["st"].split("/"))
            st = date(y, m, d)
            if v["datePeremption"] > st:
                logger.warning(
                    f"{k}: wrong peremption for {user['uid']}: "
                    f"{v['datePeremption']:%d/%m/%Y} > {st:%d/%m/%Y}"
                )
            if v["datePeremption"] < TODAY:
                logger.warning(f"{k}: obsolete data:  {v['datePeremption']:%d/%m/%Y}")
