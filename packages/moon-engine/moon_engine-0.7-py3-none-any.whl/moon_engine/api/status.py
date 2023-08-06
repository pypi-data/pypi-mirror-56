# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Status API"""
import hug
from moon_engine.api import configuration

@hug.local()
@hug.get("/status/")
def list_status():
    """
    List statuses
    :return: JSON status output
    """

    return {"status": {
        "uuid": configuration.get_configuration("uuid"),
        "type": configuration.get_configuration("type"),
        "log" : configuration.get_configuration("logging").get(
            "handlers", {}).get("file", {}).get("filename", "")
    }}
