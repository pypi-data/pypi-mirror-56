# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Import JSON API"""
import hug


@hug.local()
@hug.post("/import/")
def import_json(body):
    """Import data into the cache of the pipeline

    :return: OK if imported
    """
    if "attributes" in body:
        description = "Will update " + ", ".join(body.get("attributes"))
    else:
        description = "Will update all attributes"
    # FIXME: dev the real import functionality
    return {"status": "OK", "description": description}
