# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import logging
from moon_utilities import exceptions
from moon_utilities.security_functions import enforce
from moon_engine.api.orchestration.managers import Managers

logger = logging.getLogger("moon.manager.api.orchestration.pod")


class SlaveManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.SlaveManager = self

    @enforce(("read", "write"), "slaves")
    def update_slave(self, user_id, slave_id, value):
        self.driver.update_slave(slave_id=slave_id, value=value)

    @enforce("write", "slaves")
    def delete_slave(self, user_id, slave_id):
        self.driver.delete_slave(slave_id=slave_id)

    @enforce("write", "slaves")
    def add_slave(self, user_id, slave_id=None, data=None):
        if not slave_id:
            slave_id = uuid4().hex
        self.driver.add_slave(slave_id=slave_id, data=data)

    @enforce("read", "slaves")
    def get_slaves(self, user_id, slave_id=None):
        self.driver.get_slaves(slave_id=slave_id)
