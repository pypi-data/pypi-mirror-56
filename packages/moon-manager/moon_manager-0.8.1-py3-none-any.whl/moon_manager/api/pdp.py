# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
PDP are Policy Decision Points.

"""

import hug
import json
import logging
import requests
from moon_manager.api import ERROR_CODE
from moon_manager import db_driver
from moon_utilities.auth_functions import api_key_authentication
from moon_manager import orchestration_driver
from moon_utilities import exceptions
from moon_utilities.security_functions import validate_input
from moon_utilities.invalided_functions import invalidate_pdp_in_slaves
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class PDP(object):
    """
    Endpoint for pdp requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/pdp/", requires=api_key_authentication)
    @hug.get("/pdp/{uuid}", requires=api_key_authentication)
    def get(uuid: hug.types.uuid = None, authed_user: hug.directives.user = None):
        """Retrieve all pdp

        :param uuid: uuid of the pdp
        :param authed_user: the name of the authenticated user
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "vim_project_id": "vim_project_id1",
                "description": "... (optional)",
            }
        }
        :internal_api: get_pdp
        """
        if uuid:
            uuid = str(uuid).replace("-", "")
        data = db_driver.PDPManager.get_pdp(moon_user_id=authed_user, pdp_id=uuid)

        return {"pdps": data}

    @staticmethod
    @hug.local()
    @hug.post("/pdp/", requires=api_key_authentication)
    def post(body: validate_input("name"), response, authed_user: hug.directives.user = None):
        """Create pdp.

        :param body: preformed body from Hug
        :param response: preformed response from Hug
        :param authed_user: the name of the authenticated user
        :request body: {
            "name": "name of the PDP (mandatory)",
            "security_pipeline": ["may be empty"],
            "vim_project_id": "vim_project_id1 (may be empty)",
            "description": "description of the PDP (optional)",
        }
        :return: {
            "pdp_id1": {
                "name": "...",
                "security_pipeline": [...],
                "vim_project_id": "vim_project_id1",
                "description": "... (optional)",
            }
        }
        :internal_api: add_pdp
        """
        if not body.get("security_pipeline"):
            body["security_pipeline"] = []
        if not body.get("vim_project_id"):
            body["vim_project_id"] = None
        data = db_driver.PDPManager.add_pdp(
            moon_user_id="admin", pdp_id=None, value=body)
        uuid = list(data.keys())[0]
        if body["vim_project_id"] and body["security_pipeline"]:
            orchestration_driver.PipelineManager.add_pipeline(
                moon_user_id=authed_user, pipeline_id=uuid, data=data[uuid])
        return {"pdps": db_driver.PDPManager.get_pdp(moon_user_id=authed_user)}

    @staticmethod
    @hug.local()
    @hug.delete("/pdp/{uuid}", requires=api_key_authentication)
    def delete(uuid: hug.types.uuid, response=None, authed_user: hug.directives.user = None):
        """Delete a pdp

        :param uuid: uuid of the pdp to delete
        :param response: preformed response from Hug
        :param authed_user: the name of the authenticated user
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_pdp
        """
        uuid = str(uuid).replace("-", "")
        data = db_driver.PDPManager.delete_pdp(moon_user_id=authed_user, pdp_id=uuid)

        LOGGER.info(data)

        orchestration_driver.PipelineManager.delete_pipeline(moon_user_id=authed_user, pipeline_id=uuid)
        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_pdp_in_slaves(slaves=slaves, pdp_id=uuid)
        return {"result": True}


    @staticmethod
    @hug.local()
    @hug.patch("/pdp/{uuid}", requires=api_key_authentication)
    def patch(uuid: hug.types.uuid, body: validate_input("name"), response,
              authed_user: hug.directives.user = None):
        """Update a pdp

        :param uuid: uuid of the pdp to delete
        :param body: preformed body from Hug
        :param response: preformed response from Hug
        :param authed_user: the name of the authenticated user
        :return: {
            "pdp_id1": {
                "name": "name of the PDP",
                "security_pipeline": ["may be empty"],
                "vim_project_id": "vim_project_id1 (may be empty)",
                "description": "description of the PDP (optional)",
            }
        }
        :internal_api: update_pdp
        """

        uuid = str(uuid).replace("-", "")
        prev_data = db_driver.PDPManager.get_pdp(
            moon_user_id=authed_user, pdp_id=uuid)
        if not prev_data:
            response.status = ERROR_CODE[400]
            return {"message": "The PDP is unknown."}
        data = db_driver.PDPManager.update_pdp(
            moon_user_id=authed_user, pdp_id=uuid, value=body).get(uuid)
        if prev_data.get("security_pipeline") != data.get("security_pipeline"):
            orchestration_driver.PipelineManager.update_pipeline(moon_user_id=authed_user,
                                                                 pipeline_id=uuid,
                                                                 data=data)
        elif prev_data.get("vim_project_id") != data.get("vim_project_id"):
            orchestration_driver.PipelineManager.update_pipeline(moon_user_id=authed_user,
                                                                 pipeline_id=uuid,
                                                                 data=data)
        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_pdp_in_slaves(slaves=slaves, pdp_id=uuid, is_delete=False, data=data)

        return {"pdps": db_driver.PDPManager.get_pdp(moon_user_id=authed_user, pdp_id=uuid)}


PDPAPI = hug.API(name='pdps', doc=PDP.__doc__)


@hug.object(name='pdps', version='1.0.0', api=PDPAPI)
class PDPCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _pdps = requests.get("{}/pdp".format(db_conf.get("url")),
                             headers={"x-api-key": manager_api_key}
                            )
        if _pdps.status_code == 200:
            if name_or_id:
                _pdp = None
                if name_or_id in _pdps.json().get("pdps"):
                    _pdp = _pdps.json().get("pdps").get(name_or_id)
                else:
                    for _pdp_key in _pdps.json().get("pdps"):
                        if _pdps.json().get("pdps").get(_pdp_key).get("name") == name_or_id:
                            _pdp = _pdps.json().get("pdps").get(_pdp_key)
                            name_or_id = _pdp_key
                            break
                if not _pdp:
                    raise Exception("Cannot find PDP with name or ID {}".format(name_or_id))
                return {"pdps": [{name_or_id: _pdp}]}
            return _pdps.json()
        LOGGER.error('Cannot list PDP {}'.format(_pdps.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, description="", security_pipeline="", vim_project_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        security_pipeline = security_pipeline.split(",")
        _pdps = requests.post(
            "{}/pdp".format(db_conf.get("url")),
            json={
                "name": name,
                "security_pipeline": security_pipeline,
                "vim_project_id": vim_project_id,
                "description": description,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _pdps.status_code == 200:
            LOGGER.warning('Create {}'.format(_pdps.content))
            return _pdps.json()
        LOGGER.error('Cannot create {}'.format(name, _pdps.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name='default'):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _pdps = PDPCLI.list()
        for _slave_id, _slave_value in _pdps.get("pdps").items():
            if _slave_value.get("name") == name:
                req = requests.delete(
                    "{}/pdp/{}".format(db_conf.get("url"), _slave_id),
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find PDP with name {}".format(name))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name))
            return True
        LOGGER.error("Cannot delete PDP with name {}".format(name))
        return False

    @staticmethod
    @hug.object.cli
    def update(name, description=None, security_pipeline=None, vim_project_id=None):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _pdps = PDPCLI.list()

        for _slave_id, _slave_value in _pdps.get("pdps").items():
            if _slave_value.get("name") == name:
                description_updated = _slave_value.get("description")
                security_pipeline_updated = _slave_value.get("security_pipeline") 
                vim_project_id_updated = _slave_value.get("vim_project_id") 
                
                if description is not None:
                    description_updated = description
                if security_pipeline is not None:
                    if security_pipeline == "":
                        security_pipeline_updated = []
                    else:
                        security_pipeline_updated = security_pipeline.split(",")
                if vim_project_id is not None:
                    vim_project_id_updated = vim_project_id
                    
                req = requests.patch(
                    "{}/pdp/{}".format(db_conf.get("url"), _slave_id),
                    json={
                        "name": name,
                        "security_pipeline": security_pipeline_updated,
                        "vim_project_id": vim_project_id_updated,
                        "description": description_updated,
                    },
                    headers={
                        "x-api-key": manager_api_key,
                        "Content-Type": "application/json"
                    }
                )

        if req.status_code == 200:
            LOGGER.warning('Updated {}'.format(name))
            return True
        LOGGER.error('Cannot update PDP {}'.format(req.status_code))
        return False

    # FIXME: not tested
    # @staticmethod
    # @hug.object.cli
    # def set_project(pdp_name, project_id):
    #     db_conf = configuration.get_configuration(key='management')
    #     manager_api_key = configuration.get_api_key_for_user("admin")
    #     _pdp = PDPCLI.get(pdp_name)
    #     _pdp_id = list(_pdp.get("pdps")[0].keys())[0]
    #     _pdp_name = _pdp.get("pdps")[0].get(_pdp_id).get("name")
    #     _pdps = requests.patch(
    #         "{}/pdp/{}".format(db_conf.get("url"), _pdp_id),
    #         json={
    #             "name": _pdp_name,
    #             "vim_project_id": project_id,
    #         },
    #         headers={
    #             "x-api-key": manager_api_key,
    #             "Content-Type": "application/json"
    #         }
    #     )
    #     if _pdps.status_code == 200:
    #         LOGGER.warning('Set project {}'.format(_pdps.content))
    #         return _pdps.json()
    #     LOGGER.error('Cannot set project {} (error: {})'.format(project_id, _pdps.status_code))
    #     return 'Cannot set project {} (error: {})'.format(project_id, _pdps.status_code)
    #
    # @staticmethod
    # @hug.object.cli
    # def add_pipeline(pdp_name, pipeline_id):
    #     db_conf = configuration.get_configuration(key='management')
    #     manager_api_key = configuration.get_api_key_for_user("admin")
    #     _pdp = PDPCLI.get(pdp_name)
    #     _pdp_id = list(_pdp.get("pdps")[0].keys())[0]
    #     _pdp_name = _pdp.get("pdps")[0].get(_pdp_id).get("name")
    #     _pdp_pipelines = _pdp.get("pdps")[0].get(_pdp_id).get("security_pipeline", [])
    #     # TODO check if pipeline exists
    #     _pdp_pipelines.append(pipeline_id)
    #     _pdps = requests.patch(
    #         "{}/pdp/{}".format(db_conf.get("url"), _pdp_id),
    #         json={
    #             "name": _pdp_name,
    #             "security_pipeline": _pdp_pipelines,
    #         },
    #         headers={
    #             "x-api-key": manager_api_key,
    #             "Content-Type": "application/json"
    #         }
    #     )
    #     if _pdps.status_code == 200:
    #         LOGGER.warning('Set project {}'.format(_pdps.content))
    #         return _pdps.json()
    #     LOGGER.error('Cannot add security pipeline {} (error: {})'.format(pipeline_id,
    #                                                                       _pdps.status_code))
    #     return 'Cannot add security pipeline {} (error: {})'.format(pipeline_id, _pdps.content)
    #
    # @staticmethod
    # @hug.object.cli
    # def delete_pipeline(pdp_name, pipeline_id):
    #     db_conf = configuration.get_configuration(key='management')
    #     manager_api_key = configuration.get_api_key_for_user("admin")
    #     _pdp = PDPCLI.get(pdp_name)
    #     _pdp_id = list(_pdp.get("pdps")[0].keys())[0]
    #     _pdp_name = _pdp.get("pdps")[0].get(_pdp_id).get("name")
    #     _pdp_pipelines = _pdp.get("pdps")[0].get(_pdp_id).get("security_pipeline")
    #     # TODO check if pipeline exists
    #     _pdp_pipelines.remove(pipeline_id)
    #     _pdps = requests.patch(
    #         "{}/pdp/{}".format(db_conf.get("url"), _pdp_id),
    #         json={
    #             "name": _pdp_name,
    #             "security_pipeline": _pdp_pipelines,
    #         },
    #         headers={
    #             "x-api-key": manager_api_key,
    #             "Content-Type": "application/json"
    #         }
    #     )
    #     if _pdps.status_code == 200:
    #         LOGGER.warning('Set project {}'.format(_pdps.content))
    #         return _pdps.json()
    #     LOGGER.error('Cannot add security pipeline {} (error: {})'.format(pipeline_id,
    #                                                                       _pdps.status_code))
    #     return 'Cannot add security pipeline {} (error: {})'.format(pipeline_id, _pdps.status_code)
