# Copyright 2019 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Global attributes allow to save a specific piece of information inside Moon

"""

import logging
import hug
import requests
from moon_manager.api import ERROR_CODE
# from moon_manager import db_driver
# from moon_manager import orchestration_driver
from moon_manager import pip_driver
from moon_manager.api import configuration
from moon_utilities import exceptions
from moon_utilities.auth_functions import init_db, api_key_authentication
from moon_manager.api import slave as slave_class
from moon_utilities.invalided_functions import invalidate_attributes_in_slaves

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class Attributes(object):
    """
    Endpoint for attributes requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/attributes/", requires=api_key_authentication)
    @hug.get("/attributes/{name}", requires=api_key_authentication)
    def get(name: str = None, authed_user: hug.directives.user = None):
        """Retrieve all attributes

        :param name: name of the attribute
        :param authed_user: the name of the authenticated user
        :return: {
            "attributes": {
                    "id": "name",
                    "value": "value1",
                    "values": ["value1", "value2"],
                    "default": "value2"
                },
                {
                    "id": "name2",
                    "value": "value4",
                    "values": ["value4", "value"3"],
                    "default": "value3"
                }
            }
        }
        """
        if not name:
            data = pip_driver.AttrsManager.get_objects(moon_user_id=authed_user, object_type=name)
        else:
            data = pip_driver.AttrsManager.get_object(moon_user_id=authed_user, object_type=name)
        return {"attributes": data}

    @staticmethod
    @hug.local()
    @hug.put("/attributes/{name}/{value}", requires=api_key_authentication)
    def put(name: str, value: str, authed_user: hug.directives.user = None):
        """Initialize an attribute.

        :param name: name of the attribute
        :param value: value of the attribute
        :param authed_user: the name of the authenticated user
        :return: {
            "attributes": {
                    "name": "value1"
                    "values": ["value1", "value2"],
                    "default": "value2"
                },
                {
                    "name": "value3"
                    "values": ["value4", "value"3"],
                    "default": "value3"
                }
            }
        }
        """
        data = pip_driver.AttrsManager.update_object(moon_user_id=authed_user,
                                                     object_id=value,
                                                     object_type=name)
        slaves = slave_class.Slaves.get().get("slaves")
        ret = invalidate_attributes_in_slaves(
            slaves,
            name)
        return {"attributes": data}

    @staticmethod
    @hug.local()
    @hug.delete("/attributes/{name}", requires=api_key_authentication)
    def delete(name: str, authed_user: hug.directives.user = None):
        """Re-initialize an attribute

        :param name: the name of the attribute
        :param authed_user: the name of the authenticated user
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        """
        data = pip_driver.AttrsManager.add_object(moon_user_id=authed_user, object_type=name)
        return {"attributes": data}


AttrsAPI = hug.API(name='attributes', doc=Attributes.__doc__)
db_conf = configuration.get_configuration(key='management')
init_db(db_conf.get("token_file"))


@hug.object(name='attributes', version='1.0.0', api=AttrsAPI)
class AttributesCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def get(name):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _attrs = requests.get("{}/attributes/{}".format(db_conf.get("url"), name),
                              headers={"x-api-key": manager_api_key}
                              )
        if _attrs.status_code == 200:
            return _attrs.json()
        else:
            LOGGER.error("An error occurs ({}): {}...".format(_attrs.status_code, _attrs.text[:80]))

    @staticmethod
    @hug.object.cli
    def list():
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _attrs = requests.get("{}/attributes".format(db_conf.get("url")),
                              headers={"x-api-key": manager_api_key}
                              )
        if _attrs.status_code == 200:
            return _attrs.json()
        else:
            LOGGER.error("An error occurs ({}): {}...".format(_attrs.status_code, _attrs.text[:80]))

    @staticmethod
    @hug.object.cli
    def init(name):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _attrs = requests.delete("{}/attributes/{}".format(db_conf.get("url"), name),
                                 headers={"x-api-key": manager_api_key}
                                 )
        if _attrs.status_code == 200:
            return _attrs.json()
        else:
            LOGGER.error("An error occurs ({}): {}...".format(_attrs.status_code, _attrs.text[:80]))

    @staticmethod
    @hug.object.cli
    def set(name, value):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _attrs = requests.put("{}/attributes/{}/{}".format(db_conf.get("url"), name, value),
                              headers={"x-api-key": manager_api_key}
                              )
        if _attrs.status_code == 200:
            return _attrs.json()
        else:
            LOGGER.error("An error occurs ({}): {}...".format(_attrs.status_code, _attrs.text[:80]))

    @staticmethod
    @hug.object.cli
    def delete(name):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _attrs = requests.delete("{}/attributes/{}".format(db_conf.get("url"), name),
                                 headers={"x-api-key": manager_api_key}
                                 )
        if _attrs.status_code == 200:
            return _attrs.json()
        else:
            LOGGER.error("An error occurs ({}): {}...".format(_attrs.status_code, _attrs.text[:80]))

