#!/usr/bin/env python3

import getpass

from matrix_client.client import MatrixClient

from greet_newcomers import get_gepetto

HOME = 'https://matrix.laas.fr'
ROOM = '#gepetto:laas.fr'

if __name__ == '__main__':
    client = MatrixClient(HOME)
    client.login(username=getpass.getuser(), password=getpass.getpass())

    room = client.rooms[client.api.get_room_id(ROOM)]
    members = [m.user_id.split(':')[0][1:] for m in room.get_joined_members() if m.user_id.endswith(':laas.fr')]

    for member in get_gepetto():
        print('v' if member in members else 'x', member)
