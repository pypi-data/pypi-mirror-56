# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Slaves are endpoint for external connectors like OpenStack

"""

import logging
import hug
import requests
from moon_manager.api import ERROR_CODE
from moon_manager import db_driver
from moon_manager import orchestration_driver
from moon_manager.api import configuration
from moon_utilities import exceptions
from moon_utilities.auth_functions import init_db, api_key_authentication

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class Slaves(object):
    """
    Endpoint for slave requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/slaves/", requires=api_key_authentication)
    @hug.get("/slaves/{uuid}", requires=api_key_authentication)
    def get(uuid: hug.types.uuid = None, authed_user: hug.directives.user = None):
        """Retrieve all slaves

        :param uuid: uuid of the pdp
        :return: {
            "slaves": {
                "XXX": {
                    "name": "...",
                    "address": "..."
                },
                "YYY": {
                    "name": "...",
                    "address": "..."
                }
            }
        }
        """
        if uuid:
            uuid = str(uuid).replace("-", "")
        data = db_driver.SlaveManager.get_slaves(moon_user_id=authed_user)

        return {"slaves": data}

    @staticmethod
    @hug.local()
    @hug.post("/slave/", requires=api_key_authentication)
    def post(body, response, authed_user: hug.directives.user = None):
        """Create a slave.

        :request body: {
            "name": "name of the slave (mandatory)",
            "address": "local_or_ssh://a.b.c.d",
            "description": "description of the slave (optional)",
        }
        :return: {
            "slaves": {
                "XXX": {
                    "name": "...",
                    "address": "..."
                },
                "YYY": {
                    "name": "...",
                    "address": "..."
                }
            }
        }
        """
        try:
            # Create the DB item
            data = db_driver.SlaveManager.add_slave(
                moon_user_id=authed_user, slave_id=None, value=body)
            uuid = list(data.keys())[0]
            # Build and run the process
            new_data = orchestration_driver.SlaveManager.add_slave(moon_user_id=authed_user,
                                                                   slave_id=uuid, data=data[uuid])
            # Update the DB item with the information from the process (port, ...)
            db_driver.SlaveManager.update_slave(
                moon_user_id=authed_user, slave_id=uuid, value=new_data)
        except AttributeError as e:
            response.status = ERROR_CODE[400]
            LOGGER.exception(e)
        except exceptions.MoonError as e:
            response.status = ERROR_CODE[e.code]

        return {"slaves": db_driver.SlaveManager.get_slaves(moon_user_id=authed_user)}

    @staticmethod
    @hug.local()
    @hug.delete("/slave/{uuid}", requires=api_key_authentication)
    def delete(uuid: hug.types.uuid, response=None, authed_user: hug.directives.user = None):
        """Delete a slave

        :param uuid: uuid of the slave to delete
        :param authed_user: authenticated user name
        :param response: response initialized by Hug
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        """
        uuid = str(uuid).replace("-", "")
        try:
            db_driver.SlaveManager.delete_slave(
                moon_user_id=authed_user, slave_id=uuid)

            orchestration_driver.SlaveManager.delete_slave(
                moon_user_id=authed_user, slave_id=uuid)

        except exceptions.MoonError as e:
            response.status = ERROR_CODE[e.code]
            return {"result": False, "description": str(e)}
        except Exception as e:
            LOGGER.exception(e)
            return {"result": False, "description": str(e)}
        return {"result": True}

    @staticmethod
    @hug.local()
    @hug.patch("/slave/{uuid}", requires=api_key_authentication)
    def patch(uuid: hug.types.uuid, body, response, authed_user: hug.directives.user = None):
        """Update a slave

        :param uuid: uuid of the slave to delete
        :param body: body content of the Hug request
        :param authed_user: authenticated user name
        :param response: response initialized by Hug
        :return: {
            "pdp_id1": {
                "name": "name of the PDP",
                "address": "local_or_ssh://a.b.c.d",
                "description": "description of the slave (optional)",
            }
        }
        """

        uuid = str(uuid).replace("-", "")
        prev_data = db_driver.SlaveManager.get_slaves(moon_user_id=authed_user, slave_id=uuid)
        if not prev_data:
            response.status = ERROR_CODE[400]
            return {"message": "The slave is unknown."}
        try:
            data = db_driver.SlaveManager.update_slave(
                moon_user_id=authed_user, slave_id=uuid, value=body)


            #TODO  kill the server using orchestration_driver

        except AttributeError as e:
            response.status = ERROR_CODE[400]
            LOGGER.exception(e)
            return {"message": str(e)}
        except exceptions.MoonError as e:
            response.status = ERROR_CODE[e.code]
            return {"message": str(e)}

        return {
            "slaves": db_driver.SlaveManager.get_slaves(moon_user_id=authed_user, slave_id=uuid)
        }


SlavesAPI = hug.API(name='slaves', doc=Slaves.__doc__)
db_conf = configuration.get_configuration(key='management')
init_db(db_conf.get("token_file"))


@hug.object(name='slaves', version='1.0.0', api=SlavesAPI)
class SlavesCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list():
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _slaves = requests.get("{}/slaves".format(db_conf.get("url")),
                               headers={"x-api-key": manager_api_key}
                               )
        if _slaves.status_code == 200:
            return _slaves.json()

    @staticmethod
    @hug.object.cli
    def add(name='default', address="local", description="", grant_if_unknown_project: bool = False):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _slaves = requests.post(
            "{}/slave".format(db_conf.get("url")),
            json={
                "name": name,
                "address": address,
                "description": description,
                "grant_if_unknown_project": grant_if_unknown_project
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _slaves.status_code == 200:
            LOGGER.warning('Create {}'.format(_slaves.content))
            return _slaves.json()
        LOGGER.error('Cannot create {}'.format(name, _slaves.content))

    @staticmethod
    @hug.object.cli
    def delete(name='default'):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _slaves = SlavesCLI.list()
        for _slave_id, _slave_value in _slaves.get("slaves").items():
            if _slave_value.get("name") == name:
                req = requests.delete(
                    "{}/slave/{}".format(db_conf.get("url"), _slave_id),
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find slave with name {}".format(name))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name))
            return True
        LOGGER.error("Cannot delete slave with name {}".format(name))
        return False

    @staticmethod
    @hug.object.cli
    def update(name='default', address=None, description=None,
               grant_if_unknown_project: hug.types.one_of(("y", "n")) = None):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _slaves = SlavesCLI.list()

        for _slave_id, _slave_value in _slaves.get("slaves").items():
            if _slave_value.get("name") == name:
                address_updated = _slave_value.get("address")
                description_updated = _slave_value.get("description")
                grant_if_unknown_project_updated = _slave_value.get("grant_if_unknown_project")

                if address is not None:
                    address_updated = address
                if description is not None:
                    description_updated = description
                if grant_if_unknown_project is not None:
                    grant_if_unknown_project_updated = True if grant_if_unknown_project in ("y", "true", "1") else False

                req = requests.patch(
                    "{}/slave/{}".format(db_conf.get("url"), _slave_id),
                    json={
                        "name": name,
                        "address": address_updated,
                        "description": description_updated,
                        "grant_if_unknown_project": grant_if_unknown_project_updated,
                    },
                    headers={
                        "x-api-key": manager_api_key,
                        "Content-Type": "application/json"
                    }
                )

        if req.status_code == 200:
            LOGGER.warning('Updated {}'.format(name))
            return True
        LOGGER.error('Cannot update {}'.format(name))
        return False