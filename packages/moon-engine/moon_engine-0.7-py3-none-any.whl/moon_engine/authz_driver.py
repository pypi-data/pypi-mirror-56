# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""Authorization compute Driver"""

import logging
from moon_engine.api import configuration
from moon_engine.api.authz import authz

LOGGER = logging.getLogger("moon.manager.authz_driver")


AuthzManager = None


class Driver:
    """
    Generic driver
    """

    def __init__(self, driver_name, engine_name):
        self.name = driver_name
        self.plug = configuration.get_authz_driver()
        self.driver = self.plug.Connector(driver_name, engine_name)


class AuthzDriver(Driver):
    """
    Driver for authorization computation
    """

    def __init__(self, driver_name, engine_name):
        super(AuthzDriver, self).__init__(driver_name, engine_name)
        self.engine = engine_name

    def get_authz(self, subject_name, object_name, action_name):
        """
        Get the result of the authorization process
        :param subject_name:
        :param object_name:
        :param action_name:
        :return:
        """
        raise NotImplementedError()  # pragma: no cover


def init():
    """Initialize the managers

    :return: nothing
    """
    global AuthzManager

    LOGGER.info("Initializing driver")
    conf = configuration.get_configuration("authorization")

    AuthzManager = authz.AuthzManager(
        AuthzDriver(conf['driver'], conf.get('url'))
    )
