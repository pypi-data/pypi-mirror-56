# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import sys
import requests
from moon_utilities import exceptions


def get(url, **kwarg):
    try:
        response = requests.get(url, **kwarg)
    except requests.exceptions.RequestException as _exc:
        raise exceptions.MoonError("request failure ", _exc)
    except Exception as _exc:
        raise exceptions.MoonError("Unexpected error ", _exc)
    return response


def put(url, json="", **kwarg):
    try:
        response = requests.put(url, json=json, **kwarg)
    except requests.exceptions.RequestException as _exc:
        raise exceptions.MoonError("request failure ", _exc)
    except Exception as _exc:
        raise exceptions.MoonError("Unexpected error ", _exc)
    return response
