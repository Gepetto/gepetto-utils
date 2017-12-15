# Greet Newcomers

## Get ready

- Get Python 3 & pip
- `pip3 install ldap3` (you might need sudo, or --user, or a virtualenv)
- `mkdir -p ~/.cache`

## Go !

- `./greet_newcomers.py`

On the first time, it will construct a database of the guys already here.

After that, on each launch, it will find the new guys, and send them a greeting mail.
The template of this mail is in `template.txt`.

## Cron job

To run this script everyday at 5 AM:

```bash
crontab -l > cronfile
echo "0 5 * * * $(which python) $(pwd)/greet_newcomers.py" >> cronfile
crontab cronfile
rm cronfile
```
