#!/usr/bin/env python3

import re
from pathlib import Path

from bibtexparser import load, loads
from bibtexparser.bibdatabase import BibDatabase
from requests import get


HAL_RE = [
    (re.compile(r'(hal|tel|inria|lirmm)-\d{8}?', re.I),
     lambda g: g),
    (re.compile(r'/\d\d/\d\d/\d\d/\d\d/'),
     lambda g: 'hal-%08i' % int(g.replace('/', ''))),
]
HAL_KEYS = ['url', 'link', 'pdf', 'video']
HAL_DICT = {}
USELESS_KEYS = {'hal_local_reference', 'hal_version', 'address', 'note', 'month'}

TEAM_NAMES = {
    'ad': ['del prete'],
    'ao': ['orthey'],
    'bt': ['tondu'],
    'cv': ['vassallo'],
    'fl': ['lamiraux', 'perrin', 'dalibard'],
    'gs': ['saurel'],
    'jpl': ['laumond'],
    'mc': ['campana'],
    'mt': ['taïx', 'ta{\\"i}x'],
    'nm': ['mansard', 'ramos', 'sol{\\`a}'],
    'or': ['roussel'],
    'os': ['stasse'],
    'psa': ['salaris'],
    'ps': ['souères', 'sou{\\`e}res'],
    'st': ['tonneau'],
    'test': ['test'],
}


def parse_hal_id(entry):
    """ Tries to find HAL_ID in an entry"""
    if 'hal_id' in entry:
        return entry['hal_id']
    for regex, ret in HAL_RE:
        for key in HAL_KEYS:
            if key in entry:
                match = regex.search(entry[key])
                if match:
                    return ret(match.group())

def get_hal_entry(hal_id, hal_db):
    """ Get the entry of HAL_ID as generated by HAL. Tries local then online """
    for key in hal_db.entries_dict.keys():
        if key.endswith(hal_id):
            return hal_db.entries_dict[key]
    url = 'https://hal.archives-ouvertes.fr/%s/bibtex' % hal_id
    r = get(url)
    r.raise_for_status()
    if 'Aucun document trouvé' in r.content.decode():
        print('fail on %s' % url)
    hal_entry = loads(r.content.decode()).entries[0]
    print('HAL_ENTRY for {ID} ({hal_id}) not found on local hal db. Got Online one.'.format(**hal_entry))
    return hal_entry


def check_hal(entry, hal_db):
    """ Checks our DB is update with HAL """
    hal_id = parse_hal_id(entry)
    if not hal_id:
        return
    HAL_DICT[hal_id] = entry
    hal_entry = get_hal_entry(hal_id, hal_db)
    keys = (set(entry.keys()) | set(hal_entry.keys())) - USELESS_KEYS
    for key in keys:
        if key not in entry:
            print('IN HAL for %s: %s = {%s},' % (entry['ID'], key, hal_entry[key]))


def header(title, lvl=1):
    c = '=' if lvl == 1 else '*' if lvl == 2 else '-'
    print(c * 20 ,'{:^20}'.format(title), c * 20)


if __name__ == '__main__':
    with open('hal.bib') as hal_file:
        hal_db = load(hal_file)
    dbs = {}
    not_in_dbs = {key: [] for key in TEAM_NAMES.keys()}
    for path in Path('bib').glob('*.bib'):
        header(path.name)
        with path.open() as f:
            dbs[path.stem] = load(f)
        for entry in dbs[path.stem].entries:
            check_hal(entry, hal_db)
    with open('gepetto.bib') as gepetto_file:
        gepetto_db = load(gepetto_file)
    for entry in hal_db.entries:
        if entry['hal_id'] in HAL_DICT:
            continue
        for initials, names in TEAM_NAMES.items():
            if any(name in entry['author'].lower() for name in names):
                not_in_dbs[initials].append((entry['link'], entry['title']))
                break
        else:
            print('IN HAL ??:', entry['hal_id'], entry['author'])
    for initials, names in TEAM_NAMES.items():
        if not_in_dbs[initials]:
            header(names[0])
            with open('diffs/%s.txt' % initials, 'w') as f:
                for url, title in not_in_dbs[initials]:
                    print(url, title, file=f)
