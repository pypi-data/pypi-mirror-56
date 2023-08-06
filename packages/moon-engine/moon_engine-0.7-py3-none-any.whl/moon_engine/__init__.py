# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


__version__ = "0.7"


def get_api_key(url, user, password):
    import requests
    from requests.auth import HTTPBasicAuth
    _url = url + "/auth"
    req = requests.get(_url, auth=HTTPBasicAuth(user, password))
    if req.status_code != 200:
        raise Exception("Cannot authenticate on {} with {}".format(_url, user))
    return req.content.decode("utf-8").strip('"')


def serve(hostname="127.0.0.1", port=8080):
    import hug
    import moon_engine.server
    hug.API(moon_engine.server).http.serve(host=hostname, port=port, display_intro=False)
