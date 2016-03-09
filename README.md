# Tools for Gepetto's website

## Bibtex

`db.py` is a little script that will check the bibtex databases in `projects:/www/html/projects/gepetto/bib` are up
to date.

For now, it will compare it to HAL's one.

### Get dependencies

Using of [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) on bash or zsh, or
[virtualfish](http://virtualfish.readthedocs.org/en/latest/index.html) is strongly recommended. Do not forget that this
project uses Python3 (→ `mkvirtualenv -p $(which python3) gepetto_website_tools_venv` / `vf new -p (which python3)
gepetto_website_tools_venv`)

Then, if you have [pip-tools](https://github.com/nvie/pip-tools):

```bash
pip-sync
```

Else:

```bash
pip install -U -r requirements.txt
```

### HOWTO use it

First, let's update hal.bib:

```bash
wget -O hal.bib 'https://api.archives-ouvertes.fr/search/LAAS-GEPETTO/?omitHeader=true&wt=bibtex&q=*&sort=submittedDate_tdate+desc&fq=collCode_s%3ALAAS-GEPETTO&defType=edismax&rows=200'
```

Then, you need to copy all bib files from `projects:/www/html/projects/gepetto/bib` to `bib`.

Finally, you can launch the script `./db.py`
