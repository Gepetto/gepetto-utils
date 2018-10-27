#!/usr/bin/env python3

import shelve
from email.mime.text import MIMEText
from getpass import getuser
from os.path import abspath, dirname, expanduser, join
from smtplib import SMTP

from ldap3 import Connection

SHELF = expanduser('~/.cache/gepetto_newcomers')


def get_gepetto():
    """
    Get the old list of Gepetto members
    """
    with shelve.open(SHELF) as shelf:
        gepetto = shelf['gepetto'] if 'gepetto' in shelf else []
    return gepetto


def whoami(gepetto):
    """
    Returns the LAAS username of the current user.
    The mail will be sent from this account
    """
    with shelve.open(SHELF) as shelf:
        me = shelf['me'] if 'me' in shelf else getuser()

    while me not in gepetto:
        print("You (%s) dont's seem to be in the Gepetto group… What's your LAAS username ?" % me)
        me = input('--> ')

    # remember this in the cache
    with shelve.open(SHELF) as shelf:
        shelf['me'] = me

    return me


def greet(to, sender):
    """
    Send a greeting email to `to`
    """
    if '@' not in sender:
        sender = '%s@laas.fr' % sender

    if '@' not in to:
        to = '%s@laas.fr' % to

    with open(join(dirname(abspath(__file__)), 'template.txt')) as f:
        msg = MIMEText(f.read())

    msg['Subject'] = 'Welcome in Gepetto !'
    msg['From'] = sender
    msg['To'] = to
    msg['Bcc'] = sender
    s = SMTP('mail.laas.fr')
    s.send_message(msg)
    s.quit()


def get_gepetto_ldap():
    """
    Get a new list of Gepetto members in the LDAP of the LAAS
    """
    conn = Connection('ldap.laas.fr', auto_bind=True)
    conn.search('dc=laas,dc=fr', '(o=gepetto)', attributes=['uid'])
    return [str(entry.uid) for entry in conn.entries]


if __name__ == '__main__':
    # Get old and new list of members
    gepetto = get_gepetto()
    gepetto_ldap = get_gepetto_ldap()

    # On the first run, old list is empty, so we just set it to the new one
    if not gepetto:
        gepetto = gepetto_ldap

    # Retrieve the login of the current user, who must already be a member
    me = whoami(gepetto)

    for guy in gepetto_ldap:
        if guy not in gepetto:
            greet(guy, me)

    # Save the new list
    with shelve.open(SHELF) as shelf:
        shelf['gepetto'] = gepetto_ldap
