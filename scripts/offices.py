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
from wand.version import VERSION_INFO

# Cache LDAP data
CACHE = Path('data/offices-ldap.json')

# Drawings constants
LOGO = 'data/logo-low-black.png'
DPCM = 300 / 2.54  # dot per cm @300DPI
WIDTH, HEIGHT = int(6 * DPCM), int(3 * DPCM)  # door labels are 6cm x 3cm
NOT_OFFICES = ['Exterieur', 'BSalleGerardBauzil']
BAT_B = 'data/bat_b.png'
MAP_POSITIONS = [
    ('B181', 1600, 830),
    ('B185', 1600, 130),
    ('B61a', 1333, 1820),
    ('B63', 1333, 1500),
    ('B65', 1333, 1320),
    ('B67', 1333, 870),
    ('B69.1', 1333, 680),
    ('B69.2', 1333, 520),
    ('B90', 0, 130),
    ('B91', 0, 280),
    ('B92', 0, 430),
    ('B94', 0, 750),
]
OPERATOR = 'modulus_add' if VERSION_INFO >= (0, 5, 6) else 'add'


class Gepettist(NamedTuple):
    """A Gepettist has a SurName and a GivenName."""
    sn: str
    gn: str

    def __str__(self):
        return f'{self.gn} {self.sn}'


class Offices:
    """A dict with rooms as key and set of Gepettists as values, defaulting to empty set."""
    def __init__(self, **offices):
        self.data = defaultdict(set)
        self.data.update(offices)

    def __str__(self):
        return '\n'.join(f'{room:5}: {", ".join(str(m) for m in members)}' for room, members in self.sorted().items())

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __iter__(self):
        yield from self.data

    def items(self):
        return self.data.items()

    def sorted(self):
        return {o: sorted(self.data[o]) for o in sorted(self.data) if o != 'Exterieur' and self.data[o]}

    def dumps(self):
        """dump a sorted dict of offices with sorted lists of members as a JSON string"""
        return dumps(self.sorted(), ensure_ascii=False, indent=2, sort_keys=True)

    @staticmethod
    def loads(s):
        """constructor from a JSON string"""
        return Offices(**{room: set(Gepettist(*m) for m in members) for room, members in loads(s).items()})


# Stuff that is wrong in LDAP… We should fix that there
WRONG_OFFICE = {
    'Exterieur': {('Steve', 'Tonneau')},
    'B63': {('Ewen', 'Dantec')},
    'B65': {('Nils', 'Hareng')},
    'B67': {('Michel', 'Aractingi')},
    'B69.1': {('Guilhem', 'Saurel'), ('Pierre', 'Fernbach')},
    'B69.2': {('Nahla', 'Tabti')},
    'B90': {('Nicolas', 'Mansard')},
    'B181': {('Médéric', 'Fourmy')},
}
WRONG_OFFICE = {k: {Gepettist(sn, gn) for (gn, sn) in v} for k, v in WRONG_OFFICE.items()}
# Fix unicode from LDAP data…
ALIAS = {
    'B67': ({Gepettist('Leziart', 'Pierre-Alexandre')}, {Gepettist('Léziart', 'P-A')}),
    'B61a': ({Gepettist('Taix', 'Michel')}, {Gepettist('Taïx', 'Michel')}),
    'B91': ({Gepettist('Soueres', 'Philippe')}, {Gepettist('Souères', 'Philippe')}),
    'B181': ({Gepettist('Ramuzat', 'Noelie')}, {Gepettist('Ramuzat', 'Noëlie')}),
}


def door_label(members, logo=True):
    """Generate the label for one office."""
    if not members:
        return
    with Image(width=WIDTH, height=HEIGHT, background=Color('white')) as img, Drawing() as draw:
        if logo:
            with Image(filename=LOGO) as logo:
                logo.transform(resize=f'{WIDTH}x{HEIGHT}')
                draw.composite(OPERATOR, 200, 0, logo.width, logo.height, logo)
        draw.font_size = 80 if len(members) >= 4 else 90
        draw.text_alignment = 'center'
        height = HEIGHT - len(members) * draw.font_size
        draw.text(int(WIDTH / 2), int(height / 2) + 65, '\n'.join(str(m) for m in sorted(members)))
        draw(img)
        return img.clone()


def offices_ldap():
    """Get a dict of Gepettists in their respective office from LDAP."""
    conn = Connection('ldap.laas.fr', auto_bind=True)
    conn.search('dc=laas,dc=fr', '(laas-mainGroup=gepetto)', attributes=['sn', 'givenName', 'roomNumber', 'st'])
    offices = Offices()
    for entry in conn.entries:
        room, gn, sn, st = str(entry.roomNumber), str(entry.givenName), str(entry.sn), str(entry.st)
        if st not in ['JAMAIS', 'NON-PERTINENT'] and date(*(int(i) for i in reversed(st.split('/')))) < date.today():
            continue  # filter out alumni
        if room == '[]':
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
    for office, (before, after) in ALIAS.items():
        offices[office] = offices[office] - before | after
    return offices


def labels(offices):
    """Generate an A4 papier with labels for the doors of Gepetto offices."""
    with Image(width=int(21 * DPCM), height=int(29.7 * DPCM)) as page, Drawing() as draw:
        for i, (office, members) in enumerate(offices.items()):
            if not members or office in NOT_OFFICES:
                continue
            label = door_label(members)
            row, col = divmod(i, 3)
            row *= HEIGHT + DPCM
            col *= WIDTH + DPCM * 0.5
            draw.composite(OPERATOR, int(col + DPCM * 0.75), int(row + DPCM), label.width, label.height, label)
        draw(page)
        page.save(filename='labels.png')


def maps(offices, fixed):
    """Generate a map with labels"""
    with Image(filename=BAT_B) as page, Drawing() as draw:
        for office, x, y in MAP_POSITIONS:
            label = door_label(offices[office], logo=False)
            if label:
                draw.composite(OPERATOR, x, y, label.width / 3, label.height / 3, label)
        draw(page)
        page.save(filename='generated_map%s.png' % ('_fixed' if fixed else ''))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true', help='update data from ldap')
    parser.add_argument('--fixed', action='store_true', help='fix LDAP data from embeded infos')
    parser.add_argument('--show', action='store_true', help='show data')
    parser.add_argument('--labels', action='store_true', help='generate door labels')
    parser.add_argument('--map', action='store_true', help='generate offices map')
    parser.add_argument('-v', '--verbose', action='count', default=0)

    args = parser.parse_args()
    logging.basicConfig(level=50 - 10 * args.verbose)

    # Collect and fix data
    if args.update or not CACHE.exists():
        logging.info(' updating team members from LDAP')
        offices = offices_ldap()
        with CACHE.open('w') as f:
            f.write(offices.dumps())
    else:
        logging.info(' using cached team members')
        with CACHE.open() as f:
            offices = Offices.loads(f.read())
    if args.fixed:
        logging.info(' fixing data')
        offices = fix_wrong_offices(offices)

    # Use collected data
    if args.show:
        logging.info(' showing data')
        print(offices)
    if args.labels:
        logging.info(' generating door labels')
        labels(offices)
    if args.map:
        logging.info(' generating map')
        maps(offices, args.fixed)
