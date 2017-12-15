# Gepetto Packages Dashboard

## APIs used

- github: https://api.github.com/orgs/stack-of-tasks/repos
- gitlab: https://eur0c.laas.fr/api/v4/projects
- redmine: https://redmine.laas.fr/projects.json

### Get dependencies

- Get Python>=3.6
- `pip3 install -U -r requirements.txt` (you might need `sudo`, or *better* `--user`, or *best* a virtualenv)

## RUN

```
rm db.sqlite3 ; and ./manage.py migrate; and ./manage.py runserver localhost:8001
```
