# Greet Newcomers

## Get ready

- $ `pip install ldap3`
- $ `mkdir -p ~/.cache`

## Go !

- `./greet_newcomers.py`

On the first time, it will construct a database of the guys already here.

After that, on each launch, it will find the new guys, and send them a greeting mail.
The template of this mail is in `template.txt`.
