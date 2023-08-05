#   -*- coding: utf-8 -*-
#
#   This file is part of SKALE.py
#
#   Copyright (C) 2019 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import logging
import urllib
import requests
import functools

from skale.wallets.common import BaseWallet


LOGGER = logging.getLogger(__name__)

ROUTES = {
    'sign': '/sign',
    'sign_and_send': '/sign-and-send',
    'address': '/address',
    'public_key': '/public-key',
}


def rpc_request(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        res = func(*args, **kwargs)
        res_json = res.json()
        if res_json['error']:
            raise RPCWalletException(res_json['error'])
        else:
            return res_json['data']
    return wrapper_decorator


class RPCWalletException(Exception):
    """Raised when remote wallet retured an error"""


class RPCWallet(BaseWallet):
    def __init__(self, url):
        self._url = url

    def _construct_url(self, host, url):
        return urllib.parse.urljoin(host, url)

    @rpc_request
    def _post(self, route, data):
        request_url = self._construct_url(self._url, route)
        return requests.post(request_url, json=data)

    @rpc_request
    def _get(self, route, data=None):
        request_url = self._construct_url(self._url, route)
        return requests.get(request_url, data=data)

    def _compose_tx_data(self, tx_dict):
        return {
            'transaction_dict': json.dumps(tx_dict)
        }

    def sign(self, tx_dict):
        data = self._post(ROUTES['sign'], self._compose_tx_data(tx_dict))
        return data['transaction_hash']

    def sign_and_send(self, tx_dict):
        data = self._post(ROUTES['sign_and_send'], self._compose_tx_data(tx_dict))
        return data['transaction_hash']

    @property
    def address(self):
        data = self._get(ROUTES['address'])
        return data['address']

    @property
    def public_key(self):
        data = self._get(ROUTES['public_key'])
        return data['public_key']
