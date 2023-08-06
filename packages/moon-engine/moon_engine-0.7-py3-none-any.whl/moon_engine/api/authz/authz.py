# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
from moon_engine.api.authz.managers import Managers

logger = logging.getLogger("moon.engine.api.authz.pipeline")


class AuthzManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.AuthzManager = self

    def get_authz(self, subject_name, object_name, action_name):
        return self.driver.get_authz(subject_name=subject_name,
                                     object_name=object_name,
                                     action_name=action_name)
