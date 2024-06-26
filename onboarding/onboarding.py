#!/usr/bin/env python3

import logging
import shelve
from datetime import date
from email.mime.text import MIMEText
from getpass import getuser
from os import environ
from pathlib import Path
from smtplib import SMTP

from ldap3 import Connection

HERE = Path(__file__).resolve().parent
SHELF = Path(environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "onboarding"


def get_gepetto():
    """
    Get the old list of Gepetto members
    """
    with shelve.open(SHELF) as shelf:
        gepetto = shelf["gepetto"] if "gepetto" in shelf else []
    return gepetto


def whoami(gepetto):
    """
    Returns the LAAS username of the current user.
    The mail will be sent from this account
    """
    with shelve.open(SHELF) as shelf:
        me = shelf["me"] if "me" in shelf else getuser()

    while me not in gepetto:
        print(
            "You (%s) dont's seem to be in the Gepetto group… What's your LAAS username ?"
            % me
        )
        me = input("--> ")

    # remember this in the cache
    with shelve.open(SHELF) as shelf:
        shelf["me"] = me

    return me


def greet(to, sender):
    """
    Send a greeting email to `to`
    """
    if "@" not in sender:
        sender = "%s@laas.fr" % sender

    if "@" not in to:
        to = "%s@laas.fr" % to

    template = HERE / "template.txt"
    if not template.exists():
        template = HERE.parent / "share" / "onboarding" / "template.txt"
    if not template.exists():
        err = f"can't find template.txt around {HERE}"
        raise RuntimeError(err)
    with template.open() as f:
        msg = MIMEText(f.read())

    msg["Subject"] = "Welcome in Gepetto !"
    msg["From"] = sender
    msg["To"] = to
    msg["Bcc"] = sender
    s = SMTP("mail.laas.fr")
    s.send_message(msg)
    s.quit()


def offboard(member, cn, sender, responsable):
    """
    Send a notification to responsable and team lead about required offboarding
    """
    if "@" not in sender:
        sender = "%s@laas.fr" % sender

    msg = MIMEText(f"{cn} finit son contrat dans 90 jours.")

    msg["Subject"] = f"[gepetto-utils] Notification fin de contrat {member}"
    msg["From"] = sender
    msg["To"] = f"responsable-gepetto@laas.fr, {responsable}"
    msg["Bcc"] = sender
    s = SMTP("mail.laas.fr")
    s.send_message(msg)
    s.quit()


def get_gepetto_ldap():
    """
    Get a new list of Gepetto members in the LDAP of the LAAS
    """
    conn = Connection("ldap.laas.fr", auto_bind=True)
    conn.search(
        "dc=laas,dc=fr",
        "(o=gepetto)",
        attributes=["uid", "cn", "laas-responsable", "st"],
    )
    return [
        (
            str(e["uid"]),
            str(e["cn"]),
            str(e["laas-responsable"]),
            (
                date(*reversed([int(i) for i in str(e["st"]).split("/")]))
                if "/" in str(e["st"])
                else None
            ),
        )
        for e in conn.entries
    ]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Get old and new list of members
    gepetto = get_gepetto()
    gepetto_ldap = get_gepetto_ldap()

    # On the first run, old list is empty, so we just set it to the new one
    if not gepetto:
        gepetto = gepetto_ldap
    gepetto_uids = [m[0] for m in gepetto]

    # Retrieve the login of the current user, who must already be a member
    me = whoami(gepetto_uids)

    for member, cn, responsable, st in gepetto_ldap:
        # Onboard newcommers
        if member not in gepetto_uids:
            logging.info(f"onboarding {cn}")
            greet(member, me)
        # prepare offboarding
        if st is not None and (st - date.today()).days == 90:
            logging.info(f"offboarding {cn}")
            offboard(member, cn, me, responsable)

    # Save the new list
    with shelve.open(SHELF) as shelf:
        shelf["gepetto"] = gepetto_ldap
