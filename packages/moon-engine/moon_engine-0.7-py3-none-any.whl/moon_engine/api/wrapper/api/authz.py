# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Authz API"""

import hug
from moon_engine.api.wrapper.router import Router


class Authz(object):
    """
        Endpoint for Authz requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/authz/{project_id}/{subject_name}/{object_name}/{action_name}")
    def get(project_id: hug.types.text, subject_name: hug.types.text, object_name: hug.types.text,
            action_name: hug.types.text):
        """Get a response on Main Authorization request

                :param project_id: uuid of the project
                :param subject_name: name of the subject or the request
                :param object_name: name of the object
                :param action_name: name of the action
                :return:
                    "result": {true or false }
                :internal_api: authz
                """

        with Router(project_id, subject_name, object_name, action_name) as router:

            response = router.auth_request()
            return response
