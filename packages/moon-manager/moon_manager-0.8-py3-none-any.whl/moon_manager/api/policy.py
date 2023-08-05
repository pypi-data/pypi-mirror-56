# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
"""
Policies are instances of security models and implement security policies

"""

import hug
import logging
import requests
from moon_manager.api import ERROR_CODE
from moon_utilities.auth_functions import api_key_authentication
from moon_manager import db_driver
from moon_utilities import exceptions
from moon_utilities.security_functions import validate_input
from moon_utilities.invalided_functions import invalidate_policy_in_slaves
from moon_manager.api import slave as slave_class
from moon_manager.api import configuration

LOGGER = logging.getLogger("moon.manager.api." + __name__)


class Policies(object):
    """
    Endpoint for policy requests
    """

    @staticmethod
    @hug.local()
    @hug.get("/policies/", requires=api_key_authentication)
    @hug.get("/policies/{uuid}", requires=api_key_authentication)
    def get(uuid: hug.types.uuid = None, authed_user: hug.directives.user = None):
        """Retrieve all policies

        :param uuid: uuid of the policy
        :param authed_user: the name of the authenticated user
        :return: {
            "policy_id1": {
                "name": "name of the policy (mandatory)",
                "model_id": "ID of the model linked to this policy",
                "genre": "authz of admin (optional, default to authz)",
                "description": "description of the policy (optional)",
            }
        }
        """
        if uuid:
            uuid = str(uuid).replace("-", "")
        data = db_driver.PolicyManager.get_policies(moon_user_id=authed_user, policy_id=uuid)

        return {"policies": data}

    @staticmethod
    @hug.local()
    @hug.post("/policies/", requires=api_key_authentication)
    def post(body: validate_input("name"), response, authed_user: hug.directives.user = None):
        """Create policy.

        :param body: preformed body from Hug
        :param response: preformed response from Hug
        :param authed_user: the name of the authenticated user
        :request body: {
            "name": "name of the policy (mandatory)",
            "model_id": "ID of the model linked to this policy",
            "genre": "authz of admin (optional, default to authz)",
            "description": "description of the policy (optional)",
        }
        :return: {
            "policy_id1": {
                "name": "name of the policy (mandatory)",
                "model_id": "ID of the model linked to this policy",
                "genre": "authz of admin (optional, default to authz)",
                "description": "description of the policy (optional)",
            }
        }
        """
        db_driver.PolicyManager.add_policy(
            moon_user_id=authed_user, policy_id=None, value=body)

        return {"policies": db_driver.PolicyManager.get_policies(moon_user_id=authed_user)}

    @staticmethod
    @hug.local()
    @hug.delete("/policies/{uuid}", requires=api_key_authentication)
    def delete(uuid: hug.types.text, response=None, authed_user: hug.directives.user = None):
        """Delete a policy

        :param uuid: uuid of the policy to delete
        :param response: preformed response from Hug
        :param authed_user: the name of the authenticated user
        :return: {
            "result": "True or False",
            "message": "optional message (optional)"
        }
        """
        uuid = str(uuid).replace("-", "")
        db_driver.PolicyManager.delete_policy(
            moon_user_id=authed_user, policy_id=uuid)
        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_policy_in_slaves(slaves=slaves, policy_id=uuid)

        return {"result": True}

    @staticmethod
    @hug.local()
    @hug.patch("/policies/{uuid}", requires=api_key_authentication)
    def patch(uuid: hug.types.uuid, body: validate_input("name"), response,
              authed_user: hug.directives.user = None):
        """Update a policy

        :param uuid: uuid of the policy to update
        :param body: preformed body from Hug
        :param response: preformed response from Hug
        :param authed_user: the name of the authenticated user
        :return: {
            "policy_id1": {
                "name": "name of the policy (mandatory)",
                "model_id": "ID of the model linked to this policy",
                "genre": "authz of admin (optional, default to authz)",
                "description": "description of the policy (optional)",
            }
        }
        """

        uuid = str(uuid).replace("-", "")
        prev_data = db_driver.PolicyManager.get_policies(moon_user_id=authed_user, policy_id=uuid)
        if not prev_data:
            response.status = ERROR_CODE[400]
            return {"message": "The policy is unknown."}
        data = db_driver.PolicyManager.update_policy(
            moon_user_id=authed_user, policy_id=uuid, value=body).get(uuid)
        slaves = slave_class.Slaves.get().get("slaves")
        invalidate_policy_in_slaves(slaves=slaves, policy_id=uuid, data=data, is_delete=False)

        return {"policies": db_driver.PolicyManager.get_policies(moon_user_id=authed_user,
                                                                 policy_id=uuid)}


PoliciesAPI = hug.API(name='policies', doc=Policies.__doc__)


@hug.object(name='policies', version='1.0.0', api=PoliciesAPI)
class PoliciesCLI(object):
    """An example of command like calls via an Object"""

    @staticmethod
    @hug.object.cli
    def list(name_or_id=""):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _policies = requests.get("{}/policies".format(db_conf.get("url")),
                                 headers={"x-api-key": manager_api_key}
                                 )
        if _policies.status_code == 200:
            if name_or_id:
                if name_or_id in _policies.json().get("policies"):
                    return {"policies": {
                            name_or_id: _policies.json().get("policies").get(name_or_id)}}
                for _policy_id in _policies.json().get("policies"):
                    if name_or_id == _policies.json().get("policies").get(_policy_id).get("name"):
                        return {"policies": {
                            _policy_id: _policies.json().get("policies").get(_policy_id)}}
                else:
                    raise Exception("Cannot find policy with name {}".format(name_or_id))
            return _policies.json()

    @staticmethod
    @hug.object.cli
    def add(name, model, description="", genre="authz"):
        from moon_manager.api import models
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _model = models.ModelsCLI.list(model).get("models")[0]
        _policies = requests.post(
            "{}/policies".format(db_conf.get("url")),
            json={
                "name": name,
                "model_id": list(_model.keys())[0],
                "genre": genre,
                "description": description,
            },
            headers={
                "x-api-key": manager_api_key,
                "Content-Type": "application/json"
            }
        )
        if _policies.status_code == 200:
            LOGGER.warning('Create {}'.format(_policies.content))
            return _policies.json()
        LOGGER.error('Cannot create {} ({})'.format(name, _policies.content))

    @staticmethod
    @hug.object.cli
    def delete(name_or_id):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _policies = PoliciesCLI.list()
        for _id, _value in _policies.get("policies").items():
            if _id == name_or_id or _value.get("name") == name_or_id:
                req = requests.delete(
                    "{}/policies/{}".format(db_conf.get("url"), _id),
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find policy with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Deleted {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot delete policy with name {}".format(name_or_id))
        return False

    @staticmethod
    @hug.object.cli
    def update(name_or_id, model_id=None, description=None, genre=None):
        db_conf = configuration.get_configuration(key='management')
        manager_api_key = configuration.get_api_key_for_user("admin")
        _policies = PoliciesCLI.list()
        for _id, _value in _policies.get("policies").items():
            if _id == name_or_id or _value.get("name") == name_or_id:
                updated_model_id = _value.get("model_id")
                updated_genre = _value.get("genre")
                updated_description = _value.get("description")

                if model_id is not None:
                    updated_model_id = model_id
                if description is not None:
                    updated_description = description
                if genre is not None:
                    updated_genre = genre

                req = requests.patch(
                    "{}/policies/{}".format(db_conf.get("url"), _id),
                    json={
                        "name": _value.get("name"),
                        "model_id": updated_model_id,
                        "genre": updated_genre,
                        "description": updated_description,
                    },
                    headers={"x-api-key": manager_api_key}
                )
                break
        else:
            LOGGER.error("Cannot find policy with name {}".format(name_or_id))
            return False
        if req.status_code == 200:
            LOGGER.warning('Updated {}'.format(name_or_id))
            return True
        LOGGER.error("Cannot update policy with name {}".format(name_or_id))
        return False
