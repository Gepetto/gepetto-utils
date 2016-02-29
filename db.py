#!/usr/bin/env python3

import bibtexparser


with open('gepetto.bib') as gepetto_file:
    gepetto = gepetto_file.read()

with open('hal.bib') as hal_file:
    hal = hal_file.read()

gepetto = bibtexparser.loads(gepetto)
hal = bibtexparser.loads(hal)
