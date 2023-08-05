# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import logging
from moon_utilities.security_functions import enforce
from moon_manager.api.db.managers import Managers
from moon_utilities import exceptions

logger = logging.getLogger("moon.db.api.slave")


class SlaveManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.SlaveManager = self

    @enforce(("read", "write"), "slave")
    def update_slave(self, moon_user_id, slave_id, value):
        if slave_id not in self.driver.get_slaves(slave_id=slave_id):
            raise exceptions.SlaveNameUnknown

        return self.driver.update_slave(slave_id=slave_id, value=value)

    @enforce(("read", "write"), "slave")
    def delete_slave(self, moon_user_id, slave_id):
        if slave_id not in self.driver.get_slaves(slave_id=slave_id):
            raise exceptions.SlaveNameUnknown
        return self.driver.delete_slave(slave_id=slave_id)

    @enforce(("read", "write"), "slave")
    def add_slave(self, moon_user_id, slave_id=None, value=None):
        if not value or 'name' not in value or not value['name'].strip():
            raise exceptions.SlaveNameUnknown

        if slave_id in self.driver.get_slaves(slave_id=slave_id):
            raise exceptions.SlaveExisting
        if not slave_id:
            slave_id = uuid4().hex

        return self.driver.add_slave(slave_id=slave_id, value=value)

    @enforce("read", "slave")
    def get_slaves(self, moon_user_id, slave_id=None):
        return self.driver.get_slaves(slave_id=slave_id)
