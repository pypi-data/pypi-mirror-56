# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from uuid import uuid4
import logging
from moon_utilities import exceptions
from moon_utilities.security_functions import enforce
from moon_manager.api.orchestration.managers import Managers

logger = logging.getLogger("moon.manager.api.orchestration.pod")


class PipelineManager(Managers):

    def __init__(self, connector=None):
        self.driver = connector.driver
        Managers.PipelineManager = self

    @enforce(("read", "write"), "pipelines")
    def update_pipeline(self, moon_user_id, pipeline_id, data):
        return self.driver.update_pipeline(pipeline_id=pipeline_id, data=data)

    @enforce("write", "pipelines")
    def delete_pipeline(self, moon_user_id, pipeline_id):
        return self.driver.delete_pipeline(pipeline_id=pipeline_id)

    @enforce("write", "pipelines")
    def add_pipeline(self, moon_user_id, pipeline_id=None, data=None):
        if not pipeline_id:
            pipeline_id = uuid4().hex
        return self.driver.add_pipeline(pipeline_id=pipeline_id, data=data)

    @enforce("read", "pipelines")
    def get_pipelines(self, moon_user_id, pipeline_id=None):
        return self.driver.get_pipelines(pipeline_id=pipeline_id)
