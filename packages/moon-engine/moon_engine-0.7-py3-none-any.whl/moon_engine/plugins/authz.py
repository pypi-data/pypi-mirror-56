# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
from moon_engine.authz_driver import AuthzDriver

PLUGIN_TYPE = "authz"
LOGGER = logging.getLogger("moon.engine.plugins.authz")


class AuthzConnector(AuthzDriver):

    def __init__(self, driver_name, engine_name):
        self.driver_name = driver_name
        self.engine_name = engine_name

    def get_authz(self, subject_name, object_name, action_name):
        # FIXME: must add the real authorization engine here
        return True


class Connector(AuthzConnector):
    pass
