#!/bin/env python3
import requests


def get(homeserver, endpoint, **kwargs):
    access_token = kwargs.get('access_token', None)
    json = kwargs.get('json', None)
    args = {'url': f'{homeserver}{endpoint}'}
    if json is not None:
        args['json'] = json
    if access_token is not None:
        args['headers'] = {"Authorization": f"Bearer {access_token}"}
    request = requests.get(**args)
    return request


def post(homeserver, endpoint, **kwargs):
    access_token = kwargs.get('access_token', None)
    json = kwargs.get('json', None)
    args = {'url': f'{homeserver}{endpoint}'}
    if json is not None:
        args['json'] = json
    if access_token is not None:
        args['headers'] = {"Authorization": f"Bearer {access_token}"}
    request = requests.post(**args)
    return request
