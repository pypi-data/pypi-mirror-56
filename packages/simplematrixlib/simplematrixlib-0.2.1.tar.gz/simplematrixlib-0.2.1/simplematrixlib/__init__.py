#   Copyright (C) 2019  Tim Stahel
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import configargparse
import os
import requests
import urllib.parse
import json
from . import api_call


def get_config(description, **kwargs):
    # call this function with noparse=True to be able to add custom options.

    XDG_CONFIG_HOME = os.environ['XDG_CONFIG_HOME']

    noparse = kwargs.get('noparse', None)
    options = kwargs.get('options', None)
    config_name = kwargs.get('config_name', 'simplematrixlib')

    parser = configargparse.Parser(
        default_config_files=[f'{XDG_CONFIG_HOME}/{config_name}/*'],
        formatter_class=configargparse.RawDescriptionHelpFormatter,
        ignore_unknown_config_file_keys=True,
        description=description)

    if options:
        for value in options:
            if value == 'homeserver':
                parser.add('-hs', '--homeserver', nargs='?', help="\
                    Homeserver URL (e.g. https://matrix.org)")
            if value == 'username':
                parser.add('-u', '--username', nargs='?', help="\
                    Username or user ID of the matrix user \
                    (e.g. @steve:matrix.org)")
            if value == 'user_id':
                parser.add('-u', '--user-id', nargs='?', help="\
                    User ID of the matrix user (e.g. @steve:matrix.org")
            if value == 'access_token':
                parser.add('-t', '--access-token', nargs='?', help="\
                    Access token to use for authentication")
            if value == 'room_alias':
                parser.add('-a', '--room_alias', nargs='?', help="Room alias")

    if noparse:
        return parser
    else:
        return parser.parse()


def login(username, password, homeserver, **kwargs):
    devicename = kwargs.get('devicename', "simplematrixlib")
    data = {
        "type": "m.login.password",
        "identifier": {
            "type": "m.id.user",
            "user": f"{username}"
        },
        "password": f"{password}",
        "initial_device_display_name": f"{devicename}"
        }
    response = api_call.post(homeserver, '/_matrix/client/r0/login',
                             data=data)
    return response['access_token']


def resolve_room_alias(homeserver, room_alias):
    room_alias = urllib.parse.quote(room_alias)
    request = requests.get(
            f'{homeserver}/_matrix/client/r0/directory/room/{room_alias}')
    return request.json()['room_id']


def get_room_members(homeserver, access_token, room_id):
    request = requests.get(
            f'{homeserver}/_matrix/client/r0/rooms/{room_id}/joined_members',
            headers={"Authorization": f"Bearer {access_token}"})
    member_list = sorted([*request.json()['joined']])
    return member_list


def set_avatar(homeserver, user_id, access_token, avatar_url):
    data = f"{'avatar_url': '{avatar_url}'}"
    request = requests.get(
            f'{homeserver}/_matrix/client/r0/profile/{user_id}/avatar_url',
            headers={"Authorization": f"Bearer {access_token}"},
            data=data)
    member_list = sorted([*request.json()['joined']])
    return member_list


def invite(homeserver, access_token, room_id, user_id):
    data = json.dumps({"user_id": f"{user_id}"})
    request = requests.post(
            f'{homeserver}/_matrix/client/r0/rooms/{room_id}/invite',
            headers={"Authorization": f"Bearer {access_token}"},
            data=data)
    return request.json()


def is_room_id(room_string):
    if room_string[0] == '!':
        return True
    elif room_string[0] == '#':
        return False
    else:
        raise ValueError('String is neither valid room ID nor alias.')
