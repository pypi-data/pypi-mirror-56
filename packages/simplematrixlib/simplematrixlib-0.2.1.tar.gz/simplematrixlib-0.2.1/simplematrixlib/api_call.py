#!/bin/env python3
import requests


def get(homeserver, endpoint, **kwargs):
    access_token = kwargs.get('access_token', None)
    data = kwargs.get('data', None)
    args = {'url': f'{homeserver}{endpoint}'}
    if data is not None:
        args['json'] = data
    if access_token is not None:
        args['headers'] = {"Authorization": f"Bearer {access_token}"}
    request = requests.get(**args)
    return request.json()


def post(homeserver, endpoint, **kwargs):
    access_token = kwargs.get('access_token', None)
    data = kwargs.get('data', None)
    args = {'url': f'{homeserver}{endpoint}'}
    if data is not None:
        args['json'] = data
    if access_token is not None:
        args['headers'] = {"Authorization": f"Bearer {access_token}"}
    request = requests.post(**args)
    return request.json()
