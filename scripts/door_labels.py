#!/usr/bin/python3
"""Generate an A4 papier with labels for the doors of Gepetto offices."""

from collections import defaultdict
from datetime import date
from typing import NamedTuple

from ldap3 import Connection
from wand.color import Color
from wand.display import display
from wand.drawing import Drawing
from wand.image import Image

LOGO = '/net/pongo/vol/vol_projects/partage_gepetto/Logos/gepetto/logo-low-black.png'
DPCM = 300 / 2.54  # dot per cm @300DPI
WIDTH, HEIGHT = int(6 * DPCM), int(3 * DPCM)  # door labels are 6cm x 3cm


class Gepettist(NamedTuple):
    """A Gepettist has a SurName and a GivenName."""
    sn: str
    gn: str

    def __str__(self):
        return f'{self.gn} {self.sn}'


# Stuff that is wrong in LDAP… We should fix that there
WRONG_OFFICE = {
    'Exterieur': {('Lexia Ambaba', 'Ledaga Leounda'), ('Joan', 'Sola'), ('Melya', 'Boukheddimi'),
                  ('Florent', 'Lamiraux'), ('Steve', 'Tonneau')},
    'B61a': {('Bruno', 'Watier')},
    'B63': {('Aurélie', 'Bonnefoy')},
    'B65': {('Nils', 'Hareng')},
    'B67': {('Gabriele', 'Fadini')},
    'B69.1': {('Ewen', 'Dantec'), ('Vincent', 'Bonnet'), ('Guilhem', 'Saurel')},
    'B90': {('Nicolas', 'Mansard')},
    'B181': {('Diane', 'Bury')},
    'B185': {('Fanny', 'Risbourg')},
}
WRONG_OFFICE = {k: {Gepettist(sn, gn) for (gn, sn) in v} for k, v in WRONG_OFFICE.items()}
# Guys with name that don't fit. Sorry, PA.
ALIAS = {'B67': ({Gepettist('Leziart', 'Pierre-Alexandre')}, {Gepettist('Leziart', 'P-A')})}


def door_label(members):
    """Generate the label for one office."""
    with Image(width=WIDTH, height=HEIGHT, background=Color('white')) as img, Drawing() as draw:
        with Image(filename=LOGO) as logo:
            logo.transform(resize=f'{WIDTH}x{HEIGHT}')
            draw.composite('add', 200, 0, logo.width, logo.height, logo)
        draw.font_size = 80 if len(members) >= 4 else 90
        draw.text_alignment = 'center'
        height = HEIGHT - len(members) * draw.font_size
        draw.text(int(WIDTH / 2), int(height / 2) + 65, '\n'.join(members))
        draw(img)
        return img.clone()


def offices_members():
    """Get a dict of Gepettists in their respective office."""
    conn = Connection('ldap.laas.fr', auto_bind=True)
    conn.search('dc=laas,dc=fr', '(laas-mainGroup=gepetto)', attributes=['sn', 'givenName', 'roomNumber', 'st'])
    offices = defaultdict(set)
    for entry in conn.entries:
        room, gn, sn, st = str(entry.roomNumber), str(entry.givenName), str(entry.sn), str(entry.st)
        if st not in ['JAMAIS', 'NON-PERTINENT'] and date(*(int(i) for i in reversed(st.split('/')))) < date.today():
            continue  # filter out alumni
        if room == '[]':
            continue  # filter out the Sans-Bureaux-Fixes
        offices[room].add(Gepettist(sn, gn))
    for woffice, wmembers in WRONG_OFFICE.items():  # Patch wrong stuff from LDAP
        offices[woffice] |= wmembers  # Add members to their rightfull office
        for wrong_office in offices:
            if wrong_office != woffice:
                offices[wrong_office] -= wmembers  # remove them from the other offices
    for office, (before, after) in ALIAS.items():
        offices[office] = offices[office] - before | after
    return {k: [str(p) for p in sorted(v)] for k, v in offices.items() if k != 'Exterieur' and v}


def labels():
    """Generate an A4 papier with labels for the doors of Gepetto offices."""
    with Image(width=int(21 * DPCM), height=int(29.7 * DPCM)) as page, Drawing() as draw:
        for i, (office, members) in enumerate(offices_members().items()):
            print(office, members)
            with door_label(members) as label:
                row, col = divmod(i, 3)
                row *= HEIGHT + DPCM
                col *= WIDTH + DPCM * 0.5
                draw.composite('add', int(col + DPCM * 0.75), int(row + DPCM), label.width, label.height, label)
        draw(page)
        page.save(filename='labels.png')


if __name__ == '__main__':
    labels()
