# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

"""
Data are elements used to create rules

* Subjects are the source of an action on an object
  (examples : users, virtual machines)
* Objects are the destination of an action
  (examples virtual machines, virtual Routers)
* Actions are what subject wants to do on an object
"""

import hug
import logging
import requests
from moon_manager import db_driver as driver
from moon_utilities.security_functions import validate_input
from moon_utilities.auth_functions import api_key_authentication
from moon_utilities.invalided_functions import invalidate_data_in_slaves
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration
from moon_manager.api import policy
from moon_manager.api import meta_data

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class SubjectData(object):
    """
    Endpoint for subject data requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/policies/{uuid}/subject_data", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/subject_data/{category_id}", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/subject_data/{category_id}/{data_id}",
             requires=api_key_authentication)
    def get(uuid: hug.types.text, category_id: hug.types.text = None,
            data_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all subject categories or a specific one if data_id is given
        for a given policy

        :param uuid: uuid of the policy
        :param category_id: uuid of the subject category
        :param data_id: uuid of the subject data
        :param authed_user: user ID who do the request
        :return: [{
            "policy_id": "policy_id1",
            "category_id": "category_id1",
            "data": {
                "subject_data_id": {
                    "name": "name of the data",
                    "description": "description of the data (optional)"
                }
            }
        }]
        :internal_api: get_subject_data
        """
        LOGGER.info("api.get {} {} {}".format(uuid, category_id, data_id))
        data = driver.PolicyManager.get_subject_data(moon_user_id=authed_user, policy_id=uuid,
                                                     category_id=category_id, data_id=data_id)
        LOGGER.info("api.get data = {}".format(data))

        return {"subject_data": data}

    @staticmethod
    @hug.local()
    @hug.post("/policies/{uuid}/subject_data/{category_id}", requires=api_key_authentication)
    def post(body: validate_input("name"), uuid: hug.types.text, category_id: hug.types.text,
             authed_user: hug.directives.user = None):
        """Create or update a subject.

        :param body: body of the request
        :param uuid: uuid of the policy
        :param category_id: uuid of the subject category
        :param authed_user: user ID who do the request
        :request body: {
            "name": "name of the data (mandatory)",
            "description": "description of the data (optional)"
        }
        :return: {
            "policy_id": "policy_id1",
            "category_id": "category_id1",
            "data": {
                "subject_data_id": {
                    "name": "name of the data (mandatory)",
                    "description": "description of the data (optional)"
                }
            }
        }
        :internal_api: add_subject_data
        """
        data = driver.PolicyManager.set_subject_data(moon_user_id=authed_user, policy_id=uuid,
                                                     category_id=category_id, value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_data_in_slaves(slaves=slaves, policy_id=uuid, category_id=category_id,
                                  data_id=None, type="subject")

        return {"subject_data": data}

    @staticmethod
    @hug.local()
    @hug.delete("/policies/{uuid}/subject_data/{category_id}/{data_id}",
                requires=api_key_authentication)
    def delete(uuid: hug.types.text, data_id: hug.types.text,
               category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Delete a subject for a given policy

        :param uuid: uuid of the policy
        :param category_id: uuid of the subject category
        :param data_id: uuid of the subject data
        :param authed_user: user ID who do the request
        :return: [{
            "result": "True or False",
            "message": "optional message (optional)"
        }]
        :internal_api: delete_subject_data
        """
        LOGGER.info("api.delete {} {}".format(uuid, data_id))
        driver.PolicyManager.delete_subject_data(moon_user_id=authed_user, policy_id=uuid,
                                                 category_id=category_id, data_id=data_id)

        slaves = slave_class.Slaves.get().get("slaves")

        invalidate_data_in_slaves(slaves=slaves, policy_id=None, category_id=None,
                                  data_id=data_id, type="subject")
        return {"result": True}


class ObjectData(object):
    """
    Endpoint for object data requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/policies/{uuid}/object_data", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/object_data/{category_id}", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/object_data/{category_id}/{data_id}",
             requires=api_key_authentication)
    def get(uuid: hug.types.text, category_id: hug.types.text = None,
            data_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all object categories or a specific one if sid is given
        for a given policy

        :param uuid: uuid of the policy
        :param category_id: uuid of the object category
        :param data_id: uuid of the object data
        :param authed_user: user ID who do the request
        :return: [{
            "policy_id": "policy_id1",
            "category_id": "category_id1",
            "data": {
                "object_data_id": {
                    "name": "name of the data",
                    "description": "description of the data (optional)"
                }
            }
        }]
        :internal_api: get_object_data
        """
        data = driver.PolicyManager.get_object_data(moon_user_id=authed_user, policy_id=uuid,
                                                    category_id=category_id, data_id=data_id)
        return {"object_data": data}

    @staticmethod
    @hug.local()
    @hug.post("/policies/{uuid}/object_data/{category_id}", requires=api_key_authentication)
    def post(body: validate_input("name"), uuid: hug.types.text, category_id: hug.types.text,
             authed_user: hug.directives.user = None):
        """Create or update a object.

        :param body: body of the request
        :param uuid: uuid of the policy
        :param category_id: uuid of the object category
        :param authed_user: user ID who do the request
        :request body: {
            "name": "name of the data (mandatory)",
            "description": "description of the data (optional)"
        }
        :return: {
            "policy_id": "policy_id1",
            "category_id": "category_id1",
            "data": {
                "object_data_id": {
                    "name": "name of the data",
                    "description": "description of the data (optional)"
                }
            }
        }
        :internal_api: add_object_data
        """
        data = driver.PolicyManager.add_object_data(moon_user_id=authed_user, policy_id=uuid,
                                                    category_id=category_id, value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_data_in_slaves(slaves=slaves, policy_id=uuid, category_id=category_id,
                                  data_id=None, type="object")


        return {"object_data": data}

    @staticmethod
    @hug.local()
    @hug.delete("/policies/{uuid}/object_data/{category_id}/{data_id}",
                requires=api_key_authentication)
    def delete(uuid: hug.types.text, data_id: hug.types.text,
               category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Delete a object for a given policy

        :param uuid: uuid of the policy
        :param category_id: uuid of the object category
        :param data_id: uuid of the object data
        :param authed_user: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_object_data
        """
        driver.PolicyManager.delete_object_data(moon_user_id=authed_user, policy_id=uuid,
                                                category_id=category_id, data_id=data_id)

        slaves = slave_class.Slaves.get().get("slaves")

        invalidate_data_in_slaves(slaves=slaves, policy_id=None, category_id=None,
                                  data_id=data_id, type="object")

        return {"result": True}


class ActionData(object):
    """
    Endpoint for action data requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/policies/{uuid}/action_data", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/action_data/{category_id}", requires=api_key_authentication)
    @hug.get("/policies/{uuid}/action_data/{category_id}/{data_id}",
             requires=api_key_authentication)
    def get(uuid: hug.types.text, category_id: hug.types.text = None,
            data_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Retrieve all action categories or a specific one if sid is given
        for a given policy

        :param uuid: uuid of the policy
        :param category_id: uuid of the action category
        :param data_id: uuid of the action data
        :param authed_user: user ID who do the request
        :return: [{
            "policy_id": "policy_id1",
            "category_id": "category_id1",
            "data": {
                "action_data_id": {
                    "name": "name of the data",
                    "description": "description of the data (optional)"
                }
            }
        }]
        :internal_api: get_action_data
        """
        data = driver.PolicyManager.get_action_data(moon_user_id=authed_user, policy_id=uuid,
                                                    category_id=category_id, data_id=data_id)

        return {"action_data": data}

    @staticmethod
    @hug.local()
    @hug.post("/policies/{uuid}/action_data/{category_id}", requires=api_key_authentication)
    def post(body: validate_input("name"), uuid: hug.types.text, category_id: hug.types.text,
             authed_user: hug.directives.user = None):
        """Create or update a action.

        :param body: body of the request
        :param uuid: uuid of the policy
        :param category_id: uuid of the action category
        :param authed_user: user ID who do the request
        :request body: {
            "name": "name of the data (mandatory)",
            "description": "description of the data (optional)"
        }
        :return: {
            "policy_id": "policy_id1",
            "category_id": "category_id1",
            "data": {
                "action_data_id": {
                    "name": "name of the data",
                    "description": "description of the data (optional)"
                }
            }
        }
        :internal_api: add_action_data
        """
        data = driver.PolicyManager.add_action_data(moon_user_id=authed_user, policy_id=uuid,
                                                    category_id=category_id, value=body)

        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_data_in_slaves(slaves=slaves, policy_id=uuid, category_id=category_id,
                                  data_id=None, type="action")

        return {"action_data": data}

    @staticmethod
    @hug.local()
    @hug.delete("/policies/{uuid}/action_data/{category_id}/{data_id}",
                requires=api_key_authentication)
    def delete(uuid: hug.types.text, data_id: hug.types.text,
               category_id: hug.types.text = None, authed_user: hug.directives.user = None):
        """Delete a action for a given policy

        :param uuid: uuid of the policy
        :param category_id: uuid of the action category
        :param data_id: uuid of the action data
        :param authed_user: user ID who do the request
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        :internal_api: delete_action_data
        """
        driver.PolicyManager.delete_action_data(moon_user_id=authed_user, policy_id=uuid,
                                                category_id=category_id, data_id=data_id)

        slaves = slave_class.Slaves.get().get("slaves")

        invalidate_data_in_slaves(slaves=slaves, policy_id=None, category_id=None,
                                  data_id=data_id, type="action")
        return {"result": True}


SubjectDataAPI = hug.API(name='subject_data', doc=SubjectData.__doc__)


@hug.object(name='subject_data', version='1.0.0', api=SubjectDataAPI)
class SubjectDataCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(policy_name_or_id, name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _data_req = requests.get(
            "{}/policies/{}/subject_data".format(db_conf.get("url"), policy_id),
            headers={"x-api-key": manager_api_key}
            )
        _data_to_return = None
        _data_list = _data_req.json().get("subject_data")
        if _data_req.status_code == 200:
            if name_or_id:
                _data = None
                for _data_item in _data_list:
                    if policy_id != _data_item["policy_id"]:
                        continue
                    for _data_key, _data_value in _data_item.get("data").items():
                        if _data_value.get("name") == name_or_id:
                            _data_to_return = _data_value
                            break
                        elif _data_key == name_or_id:
                            _data_to_return = _data_value
                            break
                if not _data_to_return:
                    raise Exception("Cannot find Subject Data with name or ID {}".format(
                        name_or_id))
                return {"subject_data": _data_to_return}
            else:
                return _data_req.json()
        LOGGER.error('Cannot list Subject Data {}'.format(_data_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, category_name_or_id, policy_name_or_id, description=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        category_id = list(meta_data.SubjectCategoriesCLI.list(category_name_or_id)
                           .get("subject_categories").keys())[0]
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _url = "{}/policies/{}/subject_data/{}".format(
            db_conf.get("url"), policy_id, category_id)
        _data_req = requests.post(
            _url,
            json={
                "name": name,
                "description": description,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _data_req.status_code == 200:
            LOGGER.warning('Create {}'.format(_data_req.content))
            return _data_req.json()
        LOGGER.error('Cannot create {}'.format(name, _data_req.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id, category_name_or_id, policy_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _subject_data = SubjectDataCLI.list(policy_name_or_id)
        category_id = list(meta_data.SubjectCategoriesCLI.list(category_name_or_id)
                           .get("subject_categories").keys())[0]
        for element in _subject_data.get("subject_data"):
            for _data_id, _data_value in element.get("data").items():
                if _data_value.get("name") == name_or_id:
                    policy_id = list(
                        policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
                    _url = "{}/policies/{}/subject_data/{}/{}".format(
                        db_conf.get("url"), policy_id, category_id, _data_id)
                    req = requests.delete(
                        _url,
                        headers={"x-api-key": manager_api_key}
                    )
                    if req.status_code == 200:
                        LOGGER.warning('Deleted {}'.format(name_or_id))
                        continue
                    LOGGER.error("Cannot delete Subject Data with name {}".format(name_or_id))


ObjectDataAPI = hug.API(name='object_data', doc=ObjectData.__doc__)


@hug.object(name='object_data', version='1.0.0', api=ObjectDataAPI)
class ObjectDataCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(policy_name_or_id, name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _data_req = requests.get(
            "{}/policies/{}/object_data".format(db_conf.get("url"), policy_id),
            headers={"x-api-key": manager_api_key}
            )
        _data_to_return = None
        _data_list = _data_req.json().get("object_data")
        if _data_req.status_code == 200:
            if name_or_id:
                _data = None
                for _data_item in _data_list:
                    if policy_id != _data_item["policy_id"]:
                        continue
                    for _data_key, _data_value in _data_item.get("data").items():
                        if _data_value.get("name") == name_or_id:
                            _data_to_return = _data_value
                            break
                        elif _data_key == name_or_id:
                            _data_to_return = _data_value
                            break
                if not _data_to_return:
                    raise Exception("Cannot find Object Data with name or ID {}".format(
                        name_or_id))
                return {"object_data": _data_to_return}
            else:
                return _data_req.json()
        LOGGER.error('Cannot list Object Data {}'.format(_data_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, category_name_or_id, policy_name_or_id, description=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        category_id = list(meta_data.ObjectCategoriesCLI.list(category_name_or_id)
                           .get("object_categories").keys())[0]
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _url = "{}/policies/{}/object_data/{}".format(
            db_conf.get("url"), policy_id, category_id)
        _data_req = requests.post(
            _url,
            json={
                "name": name,
                "description": description,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _data_req.status_code == 200:
            LOGGER.warning('Create {}'.format(_data_req.content))
            return _data_req.json()
        LOGGER.error('Cannot create {}'.format(name, _data_req.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id, category_name_or_id, policy_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _object_data = ObjectDataCLI.list(policy_name_or_id)
        category_id = list(meta_data.ObjectCategoriesCLI.list(category_name_or_id)
                           .get("object_categories").keys())[0]
        for element in _object_data.get("object_data"):
            for _data_id, _data_value in element.get("data").items():
                if _data_value.get("name") == name_or_id:
                    policy_id = list(
                        policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
                    _url = "{}/policies/{}/object_data/{}/{}".format(
                        db_conf.get("url"), policy_id, category_id, _data_id)
                    req = requests.delete(
                        _url,
                        headers={"x-api-key": manager_api_key}
                    )
                    if req.status_code == 200:
                        LOGGER.warning('Deleted {}'.format(name_or_id))
                        continue
                    LOGGER.error("Cannot delete Object Data with name {}".format(name_or_id))


ActionDataAPI = hug.API(name='action_data', doc=ActionData.__doc__)


@hug.object(name='action_data', version='1.0.0', api=ActionDataAPI)
class ActionDataCLI(object):
    """An example of command like calls via an Action"""

    @staticmethod
    @hug.object.cli
    def list(policy_name_or_id, name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _data_req = requests.get(
            "{}/policies/{}/action_data".format(db_conf.get("url"), policy_id),
            headers={"x-api-key": manager_api_key}
            )
        _data_to_return = None
        _data_list = _data_req.json().get("action_data")
        if _data_req.status_code == 200:
            if name_or_id:
                _data = None
                for _data_item in _data_list:
                    if policy_id != _data_item["policy_id"]:
                        continue
                    for _data_key, _data_value in _data_item.get("data").items():
                        if _data_value.get("name") == name_or_id:
                            _data_to_return = _data_value
                            break
                        elif _data_key == name_or_id:
                            _data_to_return = _data_value
                            break
                if not _data_to_return:
                    raise Exception("Cannot find Action Data with name or ID {}".format(
                        name_or_id))
                return {"action_data": _data_to_return}
            else:
                return _data_req.json()
        LOGGER.error('Cannot list Action Data {}'.format(_data_req.status_code))

    @staticmethod
    @hug.object.cli
    def add(name, category_name_or_id, policy_name_or_id, description=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        category_id = list(meta_data.ActionCategoriesCLI.list(category_name_or_id)
                           .get("action_categories").keys())[0]
        policy_id = list(policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
        _url = "{}/policies/{}/action_data/{}".format(
            db_conf.get("url"), policy_id, category_id)
        _data_req = requests.post(
            _url,
            json={
                "name": name,
                "description": description,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _data_req.status_code == 200:
            LOGGER.warning('Create {}'.format(_data_req.content))
            return _data_req.json()
        LOGGER.error('Cannot create {}'.format(name, _data_req.content[:40]))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id, category_name_or_id, policy_name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _action_data = ActionDataCLI.list(policy_name_or_id)
        category_id = list(meta_data.ActionCategoriesCLI.list(category_name_or_id)
                           .get("action_categories").keys())[0]
        for element in _action_data.get("action_data"):
            for _data_id, _data_value in element.get("data").items():
                if _data_value.get("name") == name_or_id:
                    policy_id = list(
                        policy.PoliciesCLI.list(policy_name_or_id).get("policies").keys())[0]
                    _url = "{}/policies/{}/action_data/{}/{}".format(
                        db_conf.get("url"), policy_id, category_id, _data_id)
                    req = requests.delete(
                        _url,
                        headers={"x-api-key": manager_api_key}
                    )
                    if req.status_code == 200:
                        LOGGER.warning('Deleted {}'.format(name_or_id))
                        continue
                    LOGGER.error("Cannot delete Action Data with name {}".format(name_or_id))
