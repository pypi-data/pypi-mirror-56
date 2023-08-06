# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import hug
from moon_engine.api.pipeline.validator import Validator


class Authz(object):

    @staticmethod
    @hug.local()
    @hug.get("/authz/{subject_name}/{object_name}/{action_name}")
    def get(subject_name: hug.types.text, object_name: hug.types.text,
            action_name: hug.types.text, response):
        """Get a response on Main Authorization request

            :param subject_name: name of the subject or the request
            :param object_name: name of the object
            :param action_name: name of the action
            :return:
                "result": {true or false }
            :internal_api: authz
            """

        validator = Validator()
        response.status = validator.authz(subject_name, object_name, action_name)
