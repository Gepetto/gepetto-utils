# Greet Newcomers

## Get dependencies

This project is packaged with a nix flake

## Go !

- `./greet_newcomers.py`

On the first time, it will construct a database of the members already here.

After that, on each launch, it will find the newcomers, and send them a greeting mail.
The template of this mail is in `template.txt`.

## Cron job

To run this script everyday at 5 AM:

```bash
(crontab -l; echo "0 5 * * * cd $(pwd); nix run .#newcomers") | crontab -
```
