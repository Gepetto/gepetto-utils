# Tools for Gepetto's website

## Bibtex Databases

`db.py` is a little script that will check the bibtex databases in `projects:/www/html/projects/gepetto/bib` are up
to date.

For now, it will compare them to HAL's one.

### Get dependencies

- Get Python 3
- `pip3 install -U -r requirements.txt` (you might need `sudo`, or *better* `--user`, or *best* a virtualenv)

### HOWTO use it

First, let's update hal.bib:

```bash
wget -O hal.bib 'https://api.archives-ouvertes.fr/search/LAAS-GEPETTO/?omitHeader=true&wt=bibtex&q=*&sort=submittedDate_tdate+desc&fq=collCode_s%3ALAAS-GEPETTO&defType=edismax&rows=200'
```

Then, you need to copy all bib files from `projects:/www/html/projects/gepetto/bib` to `bib`.

Finally, you can launch the script `./db.py`
