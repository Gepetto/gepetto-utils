#!/usr/bin/env python3
"""Utils to manage Gepetto offices"""

import logging
from argparse import ArgumentParser
from collections import defaultdict
from datetime import date
from json import dumps, loads
from pathlib import Path
from typing import NamedTuple

from ldap3 import Connection
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

# Cache LDAP data
CACHE = Path("data/offices-ldap.json")

# Drawings constants
LOGO = "data/logo-low-black.png"
DPCM = 300 / 2.54  # dot per cm @300DPI
WIDTH, HEIGHT = int(6 * DPCM), int(3 * DPCM)  # door labels are 6cm x 3cm
NOT_OFFICES = ["Exterieur", "BSalleGerardBauzil"]
BAT_B = "data/rdc.png"
MAP_POSITIONS = [
    ("B20", 460, 50, 650, 228, -350),
    ("B19", 460, 233, 650, 412, -350),
    ("B18", 460, 420, 650, 598, -350),
    ("B17", 460, 608, 650, 785, -350),
    ("B16", 460, 793, 650, 966, -350),
    ("B10", 1410, 450, 1670, 691, 400),
    ("B08", 1410, 700, 1670, 925, 400),
    ("B06", 1410, 932, 1670, 1161, 400),
    ("B04", 1410, 1453, 1670, 1647, 400),
    ("B03", 1410, 1656, 1670, 1834, 400),
    ("B01", 1410, 2021, 1670, 2202, 400),
]


class Gepettist(NamedTuple):
    """A Gepettist has a SurName and a GivenName."""

    sn: str
    gn: str

    def __str__(self):
        return f"{self.gn} {self.sn}"


class Offices:
    """A dict with rooms as key and set of Gepettists as values, defaulting to empty set."""

    def __init__(self, **offices):
        self.data = defaultdict(set)
        self.data.update(offices)

    def __str__(self):
        return "\n".join(
            f'{room:5}: {", ".join(str(m) for m in members)}'
            for room, members in self.sorted().items()
        )

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __iter__(self):
        yield from self.data

    def items(self):
        return self.data.items()

    def sorted(self):
        return {
            o: sorted(self.data[o])
            for o in sorted(self.data)
            if o != "Exterieur" and self.data[o]
        }

    def dumps(self):
        """dump a sorted dict of offices with sorted lists of members as a JSON string"""
        return dumps(self.sorted(), ensure_ascii=False, indent=2, sort_keys=True)

    @staticmethod
    def loads(s):
        """constructor from a JSON string"""
        return Offices(
            **{
                room: set(Gepettist(*m) for m in members)
                for room, members in loads(s).items()
            }
        )


# Stuff that is wrong in LDAP… We should fix that there
WRONG_OFFICE = {
    "B04": {
        ("Vincent", "Bonnet"),
    },
    "B10": {
        ("Guilhem", "Saurel"),
        ("Thibault", "Marsan"),
    },
    "Exterieur": {
        ("Ariane", "Lalles"),
        ("Mickael", "Barbat"),
    },
}
WRONG_OFFICE = {
    k: {Gepettist(sn, gn) for (gn, sn) in v} for k, v in WRONG_OFFICE.items()
}
# Fix unicode from LDAP data…
ALIAS = {
    "B08": [
        (
            {Gepettist("Leziart", "Pierre-Alexandre")},
            {Gepettist("Léziart", "Pierre-Alexandre")},
        )
    ],
    "B17": [({Gepettist("Taix", "Michel")}, {Gepettist("Taïx", "Michel")})],
    "B19": [({Gepettist("Soueres", "Philippe")}, {Gepettist("Souères", "Philippe")})],
}


def door_label(members, logo=True):
    """Generate the label for one office."""
    if not members:
        return
    with Image(
        width=WIDTH, height=HEIGHT, background=Color("white")
    ) as img, Drawing() as draw:
        if logo:
            with Image(filename=LOGO) as li:
                li.transform(resize=f"{WIDTH}x{HEIGHT}")
                draw.composite("over", 200, 0, li.width, li.height, li)
        if len(members) > 2 or not logo:
            draw.font_size = 60
        # elif len(members) == 3:
        # draw.font_size = 75
        else:
            draw.font_size = 80
        draw.text_alignment = "center"
        height = HEIGHT - len(members) * draw.font_size
        draw.text(
            int(WIDTH / 2),
            int(height / 2) + 65,
            "\n".join(str(m) for m in sorted(members)),
        )
        draw(img)
        return img.clone()


def office_number(office):
    c = int(DPCM * 1.5)
    with Image(width=c, height=c, background=Color("white")) as img, Drawing() as draw:
        draw.font_size = 90
        draw.text_alignment = "center"
        draw.text(int(c / 2), int(c / 2), office)
        draw(img)
        return img.clone()


def offices_ldap():
    """Get a dict of Gepettists in their respective office from LDAP."""
    conn = Connection("ldap.laas.fr", auto_bind=True)
    conn.search(
        "dc=laas,dc=fr",
        "(laas-mainGroup=gepetto)",
        attributes=["sn", "givenName", "roomNumber", "st"],
    )
    offices = Offices()
    for entry in conn.entries:
        room, gn, sn, st = (
            str(entry.roomNumber),
            str(entry.givenName),
            str(entry.sn),
            str(entry.st),
        )
        if (
            st not in ["JAMAIS", "NON-PERTINENT"]
            and date(*(int(i) for i in reversed(st.split("/")))) < date.today()
        ):
            continue  # filter out alumni
        if room == "[]":
            logging.warning(f"Pas de bureau pour {gn} {sn}")
            continue  # filter out the Sans-Bureaux-Fixes
        offices[room].add(Gepettist(sn, gn))
    return offices


def fix_wrong_offices(offices):
    """Fix the dict of Gepettists in their respective office from embedded infos."""
    for woffice, wmembers in WRONG_OFFICE.items():  # Patch wrong stuff from LDAP
        offices[woffice] |= wmembers  # Add members to their rightfull office
        for wrong_office in offices:
            if wrong_office != woffice:
                offices[wrong_office] -= wmembers  # remove them from the other offices
    for office, aliases in ALIAS.items():
        for before, after in aliases:
            offices[office] = offices[office] - before | after
    return offices


def labels(offices):
    """Generate an A4 papier with labels for the doors of Gepetto offices."""
    with Image(
        width=int(21 * DPCM), height=int(29.7 * DPCM)
    ) as page, Drawing() as draw:
        for i, (office, members) in enumerate(offices.items()):
            if not members or office in NOT_OFFICES:
                continue
            label = door_label(members)
            row, col = divmod(i, 3)
            row *= HEIGHT + DPCM
            col *= WIDTH + DPCM * 0.5
            draw.composite(
                "over",
                int(col + DPCM * 0.75),
                int(row + DPCM),
                label.width,
                label.height,
                label,
            )
        draw(page)
        page.save(filename="labels.png")


def maps(offices, fixed):
    """Generate a map with labels"""
    with Image(filename=BAT_B) as page, Drawing() as draw:
        for office, x1, y1, x2, y2, shift in MAP_POSITIONS:
            for i, img in enumerate(
                (office_number(office), door_label(offices[office], logo=False)),
            ):
                if img:
                    width = img.width / 2
                    height = img.height / 2
                    x = (x1 + x2 - width) / 2 + shift * i
                    y = (y1 + y2 - height) / 2
                    draw.composite("over", x, y, width, height, img)
                else:
                    logging.warning(f"no label for {office}")
        draw(page)
        page.save(filename="generated_map%s.png" % ("_fixed" if fixed else ""))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="update data from ldap")
    parser.add_argument(
        "--fixed", action="store_true", help="fix LDAP data from embeded infos"
    )
    parser.add_argument("--show", action="store_true", help="show data")
    parser.add_argument("--labels", action="store_true", help="generate door labels")
    parser.add_argument("--map", action="store_true", help="generate offices map")
    parser.add_argument("-v", "--verbose", action="count", default=0)

    args = parser.parse_args()
    logging.basicConfig(level=50 - 10 * args.verbose)

    # Collect and fix data
    if args.update or not CACHE.exists():
        logging.info(" updating team members from LDAP")
        offices = offices_ldap()
        with CACHE.open("w") as f:
            f.write(offices.dumps())
    else:
        logging.info(" using cached team members")
        with CACHE.open() as f:
            offices = Offices.loads(f.read())
    if args.fixed:
        logging.info(" fixing data")
        offices = fix_wrong_offices(offices)

    # Use collected data
    if args.show:
        logging.info(" showing data")
        print(offices)
    if args.labels:
        logging.info(" generating door labels")
        labels(offices)
    if args.map:
        logging.info(" generating map")
        maps(offices, args.fixed)
