# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Test hug API (local, command-line, and HTTP access)"""
import hug


@hug.local()
@hug.get("/logs/")
def list_logs():
    """List logs

    :return: JSON status output
    """

    return {"logs": []}
